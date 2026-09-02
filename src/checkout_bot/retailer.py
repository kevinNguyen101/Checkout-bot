import asyncio
import random
import uuid

from .models import Cart, CartItem, Product, PurchaseResult

class SimulatedRetailer:
    """
    Simulated online retailer.

    A simple retailer to test the bot
    """
    def __init__(self, products: list[Product]):
        self.products = {
            product.product_id: product
            for product in products
        }

        self._lock = asyncio.Lock()
    async def get_product(self, product_id: str) -> Product | None:
        await asyncio.sleep(random.uniform(0.005, 0.020))

        product = self.products.get(product_id)

        if product is None:
            return None

        return Product(
            product_id=product.product_id,
            name=product.name,
            variant=product.variant,
            price=product.price,
            inventory=product.inventory,
        )

    async def add_to_cart(
            self,
            product_id: str,
            quantity: int,
    ) -> Cart | None:
        await asyncio.sleep(random.uniform(0.005, 0.020))

        async with self._lock:
            product = self.products.get(product_id)

            if product is None:
                return None

            if product.inventory < quantity:
                return None

            return Cart(
                items=[
                    CartItem(
                        product_id=product.product_id,
                        variant=product.variant,
                        quantity=quantity,
                        unit_price=product.price,
                    )
                ]
            )

    async def checkout(self, cart: Cart) -> PurchaseResult:
        await asyncio.sleep(random.uniform(0.010, 0.030))

        async with self._lock:
            for item in cart.items:
                product = self.products.get(item.product_id)

                if product is None:
                    return PurchaseResult(
                        success=False,
                        error="Product no longer exists",
                    )

                if product.inventory < item.quantity:
                    return PurchaseResult(
                        success=False,
                        error="Insufficient inventory",
                    )
            for item in cart.items:
                self.products[item.product_id].inventory -= item.quantity

            order_id = str(uuid.uuid4())
            return PurchaseResult(
                success=True,
                order_id=order_id,
                total=cart.total,
            )

    async def restock(
        self,
        product_id: str,
        quantity: int,
    ) -> None:
        async with self._lock:
            product = self.products.get(product_id)

            if product is not None:
                product.inventory += quantity