from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from school_api.extensions import db, bcrypt
from school_api.models.user import User
from datetime import datetime
import os
import logging

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

logging.basicConfig(level=logging.DEBUG)

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'innerman@gmail.com')  
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'innerman_school')  

@auth.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        print("Received data:", data)

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('user_type')

        if user_type == 'admin':
            return jsonify({'error': 'Cannot register as admin'}), 403

        if not all([first_name, last_name, email, password, user_type]):
            return jsonify({'error': 'Missing required fields'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already in use'}), 409

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            user_type=user_type
        )

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)
        return jsonify({
            'user': {
                'id': new_user.id,
                'username': new_user.get_full_name(),
                'email': new_user.email,
                'access_token': access_token,
                'type': new_user.user_type
            },
            'message': 'User registered successfully'
        }), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    logging.debug(f"Received login data: {data}")

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        response = {
            'access_token': access_token,
            'user_id': user.id,
            'user_type': user.user_type
        }
        logging.debug(f"Login successful for user_id: {user.id}")
        return jsonify(response), 200

    logging.error("Invalid credentials")
    return jsonify({"error": "Invalid credentials"}), 401

@auth.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500


@auth.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': 'User not found'}), 404

        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized access'}), 403

        users = User.query.all()
        serialized_users = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'user_type': user.user_type,
            'isadmin': user.isadmin,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } for user in users]

        return jsonify({'users': serialized_users}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
