from flask import Blueprint, jsonify, request
from models import Order
from extensions import db


# Orders Blueprints
orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data.get('user_id')
    products = data.get('products')

    if not user_id or not products:
        return jsonify({'message': 'User ID and products are required'}), 400

    new_order = Order(user_id=user_id, products=products)
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order created', 'order_id': new_order.id}), 201

@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    orders_list = []
    for order in orders:
        orders_list.append({
            'id': order.id,
            'user_id': order.user_id,
            'products': order.products,
            'status': order.status,
            'created_at': order.created_at,
            'modified_at': order.modified_at
        })
    return jsonify(orders_list), 200

@orders_bp.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    order_data = {
        'id': order.id,
        'user_id': order.user_id,
        'products': order.products,
        'status': order.status,
        'created_at': order.created_at,
        'modified_at': order.modified_at
    }
    return jsonify(order_data), 200


@orders_bp.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    data = request.get_json()
    order.status = data.get('status', order.status)

    db.session.commit()

    return jsonify({'message': 'Order updated'}), 200


@orders_bp.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({'message': 'Order deleted'}), 200