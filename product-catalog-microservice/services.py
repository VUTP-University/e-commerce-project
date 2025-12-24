from models import Product
from extensions import db


def increase_stock(sku: str, amount: int) -> Product:
    if amount <= 0:
        raise ValueError("Amount must be positive")

    sku = sku.strip().upper()
    product = Product.query.filter_by(sku=sku).first()

    if not product:
        raise LookupError("Product not found")

    product.stock += amount
    db.session.commit()

    return product


def decrease_stock(sku: str, amount: int) -> Product:
    if amount <= 0:
        raise ValueError("Amount must be positive")

    sku = sku.strip().upper()
    product = Product.query.filter_by(sku=sku).first()

    if not product:
        raise LookupError("Product not found")

    if product.stock < amount:
        raise ValueError("Insufficient stock")

    product.stock -= amount
    db.session.commit()

    return product
