from flask import Blueprint, request, jsonify
from services import increase_stock, decrease_stock

product_bp = Blueprint("product_bp", __name__)


@product_bp.route("/products/<string:sku>/increase", methods=["POST"])
def increase_stock_route(sku):
    data = request.get_json()
    amount = data.get("amount")

    if amount is None:
        return jsonify({"error": "Amount is required"}), 400

    try:
        product = increase_stock(sku, amount)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except LookupError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify({
        "sku": product.sku,
        "stock": product.stock
    }), 200


@product_bp.route("/products/<string:sku>/decrease", methods=["POST"])
def decrease_stock_route(sku):
    data = request.get_json()
    amount = data.get("amount")

    if amount is None:
        return jsonify({"error": "Amount is required"}), 400

    try:
        product = decrease_stock(sku, amount)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except LookupError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify({
        "sku": product.sku,
        "stock": product.stock
    }), 200
