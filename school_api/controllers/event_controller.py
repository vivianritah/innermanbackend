from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from school_api.extensions import db
from school_api.models.event import Event
from school_api.decorators import admin_required

events = Blueprint('events', __name__, url_prefix='/api/v1/events')

@events.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_event():
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description')
        date = data.get('date')
        location = data.get('location')

        if not name:
            return jsonify({'error': 'Name is required'}), 400
        if not description:
            return jsonify({'error': 'Description is required'}), 400
        if not date:
            return jsonify({'error': 'Date is required'}), 400
        if not location:
            return jsonify({'error': 'Location is required'}), 400

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
        return jsonify({'error': str(e)}), 500
# Get all events
@events.route('/', methods=['GET'])
@jwt_required()
def get_events():
    try:
        events = Event.query.all()
        return jsonify([{
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'date': event.date,
            'location': event.location,
            'user_id': event.user_id
        } for event in events]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get a single event by ID
@events.route('/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event(event_id):
    try:
        event = Event.query.get_or_404(event_id)
        return jsonify({
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'date': event.date,
            'location': event.location,
            'user_id': event.user_id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

0

# Update an event
@events.route('/<int:event_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_event(event_id):
    try:
        data = request.json
        event = Event.query.get_or_404(event_id)
        
        event.name = data.get('name', event.name)
        event.description = data.get('description', event.description)
        event.date = datetime.fromisoformat(data.get('date', event.date.isoformat()))
        event.location = data.get('location', event.location)

        db.session.commit()
        return jsonify({'message': 'Event updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete an event
@events.route('/<int:event_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_event(event_id):
    try:
        event = Event.query.get_or_404(event_id)

        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500