from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import Product

product_bp = Blueprint("product_bp", __name__)


@product_bp.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()

    sku = data["sku"].strip().upper()
    name = data["name"].strip()
    stock = int(data["stock"])

    product = Product(sku=sku, name=name, stock=stock)

    try:
        db.session.add(product)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Product with this SKU already exists"}), 409

    return jsonify({"message": "Product created"}), 201


@product_bp.route("/products", methods=["GET"])
def list_products():
    products = Product.query.all()
    return jsonify([
        {"sku": p.sku, "name": p.name, "stock": p.stock}
        for p in products
    ])
