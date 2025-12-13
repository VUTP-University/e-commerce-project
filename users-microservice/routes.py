from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services import generate_token
from models import User, Address
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


# Auth Blueprint
auth_bp = Blueprint('auth', __name__)
# Address Blueprint
address_bp = Blueprint('address', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        token = generate_token(identity=user.id)
        return jsonify({"token": token,
                        "user_id": user.id,
                        "username": user.username}), 200

    return jsonify({"msg": "Invalid credentials"}), 401


@auth_bp.route('/all_users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(user_list), 200

  
      email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = generate_token(identity=user.id)
    return jsonify({"access_token": access_token, "msg": "Login successful"}), 200


@address_bp.route('/addresses', methods=['POST'])
@jwt_required()
def create_address():
    """Create a new shipping address for the authenticated user"""
    data = request.get_json()
    
    # Validate required fields
    street = data.get('street')
    city = data.get('city')
    zip_code = data.get('zip')
    country = data.get('country')
    
    if not street or not city or not zip_code or not country:
        return jsonify({"msg": "Missing required fields: street, city, zip, country"}), 400
    
    # Get authenticated user ID
    user_id = get_jwt_identity()
    
    # Verify user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    # Create new address
    new_address = Address(
        user_id=user_id,
        street=street,
        city=city,
        zip=zip_code,
        country=country
    )
    
    db.session.add(new_address)
    db.session.commit()
    
    return jsonify({
        "msg": "Address created successfully",
        "address": {
            "id": new_address.id,
            "street": new_address.street,
            "city": new_address.city,
            "zip": new_address.zip,
            "country": new_address.country,
            "created_at": new_address.created_at.isoformat()
        }
    }), 201


@address_bp.route('/addresses', methods=['GET'])
@jwt_required()
def get_addresses():
    """Get all shipping addresses for the authenticated user"""
    user_id = get_jwt_identity()
    
    # Get all addresses for the user
    addresses = Address.query.filter_by(user_id=user_id).all()
    
    addresses_list = [{
        "id": addr.id,
        "street": addr.street,
        "city": addr.city,
        "zip": addr.zip,
        "country": addr.country,
        "created_at": addr.created_at.isoformat()
    } for addr in addresses]
    
    return jsonify({
        "msg": "Addresses retrieved successfully",
        "addresses": addresses_list,
        "count": len(addresses_list)
    }), 200


@address_bp.route('/addresses/<address_id>', methods=['PUT'])
@jwt_required()
def update_address(address_id):
    """Update a specific shipping address"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Find the address
    address = Address.query.get(address_id)
    
    if not address:
        return jsonify({"msg": "Address not found"}), 404
    
    # Verify the address belongs to the authenticated user
    if address.user_id != user_id:
        return jsonify({"msg": "Unauthorized to modify this address"}), 403
    
    # Update fields if provided
    if 'street' in data:
        address.street = data['street']
    if 'city' in data:
        address.city = data['city']
    if 'zip' in data:
        address.zip = data['zip']
    if 'country' in data:
        address.country = data['country']
    
    db.session.commit()
    
    return jsonify({
        "msg": "Address updated successfully",
        "address": {
            "id": address.id,
            "street": address.street,
            "city": address.city,
            "zip": address.zip,
            "country": address.country,
            "created_at": address.created_at.isoformat()
        }
    }), 200


@address_bp.route('/addresses/<address_id>', methods=['DELETE'])
@jwt_required()
def delete_address(address_id):
    """Delete a specific shipping address"""
    user_id = get_jwt_identity()
    
    # Find the address
    address = Address.query.get(address_id)
    
    if not address:
        return jsonify({"msg": "Address not found"}), 404
    
    # Verify the address belongs to the authenticated user
    if address.user_id != user_id:
        return jsonify({"msg": "Unauthorized to delete this address"}), 403
    
    db.session.delete(address)
    db.session.commit()
    
    return jsonify({"msg": "Address deleted successfully"}), 200