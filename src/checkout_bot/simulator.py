import asyncio
import random
from typing import Callable, Awaitable

from .events import InventoryEvent, InventoryEventType
from .retailer import SimulatedRetailer


EventCallback = Callable[
    [InventoryEvent],
    Awaitable[None],
]


class InventorySimulator:

    def __init__(
            self,
            retailer: SimulatedRetailer,
            product_ids: list[str],
            event_interval: tuple[float, float] = (1.0, 3.0),
            seed: int | None = None,
    ):
        self.retailer = retailer
        self.product_ids = product_ids

        self.event_interval = event_interval

        self.random = random.Random(seed)

        self.running = True

        self.callback: EventCallback | None = None

    def set_callback(
        self,
        callback: EventCallback
    ) -> None:
        self.callback = callback

    async def generate_event(
            self,
    ) -> InventoryEvent:

        product_id = self.random.choice(
            self.product_ids
        )

        event_type = self.random.choices(
            [
                InventoryEventType.RESTOCK,
                InventoryEventType.SALE,
                InventoryEventType.PRICE_CHANGE,
            ],
            weights=[
                50,
                35,
                15,
            ],
            k=1,
        )[0]

        if event_type == InventoryEventType.RESTOCK:

            quantity = self.random.randint(1, 5)

            return InventoryEvent(
                event_type=event_type,
                product_id=product_id,
                quantity=quantity,
            )

        if event_type == InventoryEventType.SALE:

            quantity = self.random.randint(1, 3)

            return InventoryEvent(
                event_type=event_type,
                product_id=product_id,
                quantity=quantity,
            )

        product = await self.retailer.get_product(
            product_id
        )

        if product is None:
            return InventoryEvent(
                event_type=event_type,
                product_id=product_id,
            )

        multiplier = self.random.uniform(
            0.90,
            1.10,
        )

        new_price = round(
            product.price * multiplier,
            2,
        )

        return InventoryEvent(
            event_type=event_type,
            product_id=product_id,
            new_price=new_price,
        )

    async def apply_event(
            self,
            event: InventoryEvent,
    ) -> None:

        product = await self.retailer.get_product(
            event.product_id
        )

        if product is None:
            return

        if event.event_type == InventoryEventType.RESTOCK:

            await self.retailer.restock(
                event.product_id,
                event.quantity
            )

            print(
                f"[SImulator] RESTOCK "
                f"{event.product_id} "
                f"+{event.quantity}"
            )

        elif event.event_type == InventoryEventType.SALE:

            await self.retailer.remove_inventory(
                event.product_id,
                event.quantity,
            )

            print(
                f"[Simulator] SALE "
                f"{event.product_id} "
                f"-{event.quantity}"
            )

        elif event.event_type == InventoryEventType.PRICE_CHANGE:

            await self.retailer.update_price(
                event.product_id,
                event.new_price,
            )

            print(
                f"[Simulator] PRICE_CHANGE "
                f"{event.product_id} "
                f"new_price=${event.new_price:.2f}"
            )
    async def run(self) -> None:

        if not self.product_ids:
            raise ValueError(
                "Inventory simulator requires "
                "at least one product."
            )

        while self.running:

            delay = self.random.uniform(
                *self.event_interval
            )

            await asyncio.sleep(delay)

            event = await self.generate_event()

            await self.apply_event(event)

            if self.callback is not None:
                await self.callback(event)

    def stop(self) -> None:
        self.running = False