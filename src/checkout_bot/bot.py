import asyncio
import time

from .decision import should_purchase
from .models import PurchaseTarget
from .monitor import InventoryMonitor
from .retailer import SimulatedRetailer

class CheckoutBot:
    def __init__(
            self,
            retailer: SimulatedRetailer,
            targets: list[PurchaseTarget],
            budget: float,
            poll_interval: float = 0.05,
    ):
        self.retailer = retailer
        self.targets = targets
        self.budget = budget
        self.spent = 0.0

        self.monitor = InventoryMonitor(
            retailer,
            poll_interval,
        )

        self.running = True

    async def handle_inventory(
            self,
            product,
            detected_at: float,
            target: PurchaseTarget
    ):
        decision_start = time.perf_counter()

        if not should_purchase(product, target):
            return

        if self.spent + (product.price * target.quantity) > self.budget:
            print(f"[Rejected] {product.name}: Budget exceeded")
            return

        decision_latency = (time.perf_counter() - decision_start)

        checkout_start = time.perf_counter()

        cart = await self.retailer.add_to_cart(
            product.product_id,
            target.quantity,
        )

        if cart is None:
            print(f"[Failed] {product.name}: Could not add to cart")
            return

        result = await self.retailer.checkout(cart)

        checkout_latency = (time.perf_counter() - checkout_start)

        if result.success:
            self.spent += result.total

            print(
                f"[Success] {product.name} | "
                f"order={result.order_id} | "
                f"total=${result.total:.2f} | "
                f"decision={decision_latency * 1000:.2f}ms | "
                f"checkout={checkout_latency * 1000:.2f}ms"
            )

            self.running = False
        else:
            print(
                f"[Failed] {product.name}: "
                f"{result.error}"
            )
    async def run(self):
        tasks = []

        for target in self.targets:
            async def monitor_target(target=target):
                async def callback(
                        product,
                        detected_at,
                ):
                    await self.handle_inventory(
                        product,
                        detected_at,
                        target,
                    )

                while self.running:
                    product = await self.retailer.get_product(target.product_id)

                    if product and product.inventory > 0:
                        await self.handle_inventory(
                            product,
                            time.perf_counter(),
                            target,
                        )

                    await asyncio.sleep(self.monitor.poll_interval)

            tasks.append(asyncio.create_task(monitor_target()))

        while self.running:
            await asyncio.sleep(0.01)

        for task in tasks:
            task.cancel()

        await asyncio.gather(
            *tasks,
            return_exceptions=True
        )