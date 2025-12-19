from extensions import db
from models import Product

def increase_stock(product_id: int, amount: int):
    product = Product.query.get_or_404(product_id)
    product.stock += amount
    db.session.commit()
    return product

def decrease_stock(product_id: int, amount: int):
    product = Product.query.get_or_404(product_id)

    if product.stock < amount:
        raise ValueError("Insufficient stock")

    product.stock -= amount
    db.session.commit()
    return product
