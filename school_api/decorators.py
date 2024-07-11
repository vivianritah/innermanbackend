from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from school_api.models.user import User

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not user.isadmin:
            return jsonify({'error': 'Admins only!'}), 403
        return fn(*args, **kwargs)
    return wrapper
