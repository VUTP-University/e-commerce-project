from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
# from services import generate_token 
from models import Inventory
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


# Inventory Blueprint
inventory_bp = Blueprint('inventory', __name__)

# Create new inventory item
@inventory_bp.route('/inventory', methods=['POST'])
def create_item():
    data = request.get_json()
    quantity = data.get('quantity')
    reserved = data.get('reserved', False)

    if not quantity:
        return jsonify({"msg": "Missing required fields - Quantity"}), 400

    new_item = Inventory(quantity=quantity, reserved=reserved)

    db.session.add(new_item)
    db.session.commit()

    return jsonify({"msg": "Inventory item created successfully"}), 201


# Get all inventory items
@inventory_bp.route('/inventory', methods=['GET'])
def get_items():
    items = Inventory.query.all()
    item_list = [{"product_id": item.product_id, "quantity": item.quantity, "reserved": item.reserved} for item in items]
    return jsonify(item_list), 200