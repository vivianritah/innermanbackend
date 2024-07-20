from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from school_api.extensions import db
from school_api.models.event import Event
from school_api.decorators import admin_required
from datetime import datetime

events_blueprint = Blueprint('events', __name__, url_prefix='/api/v1/events')

@events_blueprint.route('/create', methods=['POST', 'OPTIONS'])
@jwt_required()
@admin_required
def create_event():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight'}), 200

    try:
        data = request.json
        name = data.get('name')
        description = data.get('description')
        date = data.get('date')
        location = data.get('location')

        if not name or not description or not date or not location:
            return jsonify({'error': 'All fields are required'}), 400

        try:
            date = datetime.fromisoformat(date)
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

        user_id = get_jwt_identity()
        event = Event(
            name=name,
            description=description,
            date=date,
            location=location,
            user_id=user_id
        )
        db.session.add(event)
        db.session.commit()
        return jsonify({'message': 'Event created successfully'}), 201
    except Exception as e:
        current_app.logger.error(f"Error creating event: {str(e)}")
        return jsonify({'error': str(e)}), 500

@events_blueprint.route('/get_event', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_events():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight'}), 200

    try:
        current_user_id = get_jwt_identity()
        current_app.logger.debug(f"Current user ID: {current_user_id}")
        events = Event.query.filter_by(user_id=current_user_id).all()
        events_list = [event.to_dict() for event in events]
        return jsonify(events_list), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching events: {str(e)}")
        return jsonify({'error': 'Failed to fetch events'}), 500

@events_blueprint.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_event(id):
    try:
        event = Event.query.get(id)
        if event:
            return jsonify(event.to_dict()), 200
        else:
            return jsonify({'error': 'Event not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error fetching event: {str(e)}")
        return jsonify({'error': 'Failed to fetch event'}), 500
