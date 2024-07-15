from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from school_api.extensions import db, bcrypt
from school_api.models.notification import Notification

notifications = Blueprint('notifications', __name__, url_prefix='/api/v1/notifications')

@notifications.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    try:
        user_id = get_jwt_identity()
        notifications = Notification.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': notification.id,
            'message': notification.message,
            'user_id': notification.user_id,
            'timestamp': notification.timestamp,
            'is_read': notification.is_read,
            'application_id': notification.application_id
        } for notification in notifications]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notifications.route('/', methods=['POST'])
@jwt_required()
def create_notification():
    try:
        data = request.json
        message = data.get('message')
        application_id = data.get('application_id')

        if not message:
            return jsonify({'error': 'Message is required'}), 400

        user_id = get_jwt_identity()
        notification = Notification(
            message=message,
            user_id=user_id,
            application_id=application_id
        )
        db.session.add(notification)
        db.session.commit()
        return jsonify({'message': 'Notification created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notifications.route('/<int:notification_id>', methods=['PUT'])
@jwt_required()
def update_notification(notification_id):
    try:
        data = request.json
        is_read = data.get('is_read')

        user_id = get_jwt_identity()
        notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()

        if not notification:
            return jsonify({'error': 'Notification not found'}), 404

        if is_read is not None:
            notification.is_read = is_read

        db.session.commit()
        return jsonify({'message': 'Notification updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notifications.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    try:
        user_id = get_jwt_identity()
        notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()

        if not notification:
            return jsonify({'error': 'Notification not found'}), 404

        db.session.delete(notification)
        db.session.commit()
        return jsonify({'message': 'Notification deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
