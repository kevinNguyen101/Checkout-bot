import asyncio

from .bot import CheckoutBot
from .models import Product, PurchaseTarget
from .retailer import SimulatedRetailer
from .simulator import InventorySimulator

async def main():

    products =[
        Product(
            product_id="gpu-001",
            name="Example GPU",
            variant="16GB",
            price=449.99,
            inventory=0,
        ),
        Product(
            product_id="console-001",
            name="Example Console",
            variant="Standard",
            price=499.99,
            inventory=0,
        ),
        Product(
            product_id="keyboard-001",
            name="Example Keyboard",
            variant="Mechanical",
            price=129.99,
            inventory=5,
        ),
    ]

    retailer = SimulatedRetailer(products)

    targets = [
        PurchaseTarget(
            product_id="gpu-001",
            variant="16GB",
            max_price=450.00,
            quantity=1,
        ),
        PurchaseTarget(
            product_id="console-001",
            variant="Standard",
            max_price=500.00,
            quantity=1,
        ),
    ]

    bot = CheckoutBot(
        retailer=retailer,
        targets=targets,
        budget=500.00,
        poll_interval=0.05,
    )

    simulator = InventorySimulator(
        retailer=retailer,
        product_ids=[
            product.product_id
            for product in products
        ],
        event_interval=(0.5,2.0),
        seed=42
    )

    async def run_simulator():

        try:
            await simulator.run()
        except asyncio.CancelledError:
            simulator.stop()
            raise

    await asyncio.gather(
        bot.run(),
        run_simulator(),
    )

if __name__ == "__main__":
    asyncio.run(main())