from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Product:
    product_id: str
    name: str
    variant: str
    price: float
    inventory: int

@dataclass
class PurchaseTarget:
    product_id: str
    variant: str
    max_price: float
    quantity: int = 1

@dataclass
class CartItem:
    product_id: str
    variant: str
    quantity: int
    unit_price: float

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price

@dataclass
class Cart:
    items: list[CartItem] = field(default_factory=list)

    @property
    def total(self) -> float:
        return sum(item.total for item in self.items)

@dataclass
class PurchaseResult:
    success: bool
    order_id: Optional[str] = None
    total: float = 0.0
    error: Optional[str] = None