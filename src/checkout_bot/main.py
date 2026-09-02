import asyncio

from .bot import CheckoutBot
from .models import Product, PurchaseTarget
from .retailer import SimulatedRetailer


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

    async def simulate_restock():

        await asyncio.sleep(2)

        print("\n[RETAILER] GPU restocked!\n")

        await retailer.restock(
            "gpu-001",
            1,
        )
    await asyncio.gather(
        bot.run(),
        simulate_restock(),
    )

if __name__ == "__main__":
    asyncio.run(main())