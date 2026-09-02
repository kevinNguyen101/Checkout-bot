from dataclasses import dataclass
from enum import Enum
from typing import Optional


class InventoryEventType(Enum):
    Restorck = "restock"
    Sale = "sale"
    PRICE_CHANGE = "price_change"

@dataclass
class InventoryEvent:
    event_type: InventoryEventType
    product_id: str
    quantity: int = 0
    new_price: Optional[float] = None