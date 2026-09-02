from .models import Product, PurchaseTarget

def should_purchase(
        product: Product,
        target: PurchaseTarget,
) -> bool:
    if product.product_id != target.product_id:
        return False

    if product.variant != target.variant:
        return False

    if product.inventory < target. quantity:
        return False

    if product.price > target.max_price:
        return False

    return True