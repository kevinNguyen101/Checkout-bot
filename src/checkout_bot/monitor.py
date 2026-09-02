import asyncio
import time
from typing import Callable

from .models import Product
from .retailer import SimulatedRetailer

class InventoryMonitor:
    def __init__(
            self,
            retailer: SimulatedRetailer,
            poll_interval: float = 0.05,
    ):
        self.retailer = retailer
        self.poll_interval = poll_interval

    async def monitor(
        self,
        product_id: str,
        callback: Callable[[Product, float], None],
    ) -> None:
        was_in_stock = False

        while True:
            product = await self.retailer.get_product(product_id)

            if product is not None:

                in_stock = product.inventory > 0

                if in_stock and not was_in_stock:
                    detected_at = time.perf_counter()

                    callback(
                        product,
                        detected_at,
                    )
                was_in_stock = in_stock
                
            await asyncio.sleep(self.poll_interval)