from flask import Blueprint, request, jsonify
from datetime import datetime
from school_api.extensions import db
from school_api.models.application import Application
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify
from datetime import datetime
from school_api.extensions import db
from school_api.models.application import Application
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import exists
import logging

application = Blueprint('application', __name__, url_prefix='/api/v1/application')

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@application.route('/register', methods=['POST'])
def create_application():
    try:
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        required_fields = [
            'first_name', 'last_name', 'date_of_birth', 
            'name_of_previous_school', 'previous_math_grade', 'previous_english_grade', 
            'current_level', 'year_of_admission', 'guardian_full_name', 
            'guardian_contact', 'guardian_email', 'user_id'
        ]
        if not all(field in data for field in required_fields):
            logging.error("All mandatory fields must be provided.")
            return jsonify({"error": "All mandatory fields must be provided."}), 400

        # Ensure user_id is valid
        try:
            user_id = int(data['user_id'])
        except ValueError:
            logging.error("user_id must be an integer.")
            return jsonify({"error": "user_id must be an integer."}), 400

        user_exists = db.session.query(exists().where(user_id == user_id)).scalar()
        if not user_exists:
            logging.error(f"Invalid user_id: {user_id}")
            return jsonify({"error": "Invalid user_id."}), 400

        new_application = Application(
            first_name=data['first_name'],
            last_name=data['last_name'],
            other_name=data.get('other_name'),
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d'),
            name_of_previous_school=data['name_of_previous_school'],
            previous_math_grade=data['previous_math_grade'],
            previous_english_grade=data['previous_english_grade'],
            current_level=data['current_level'],
            year_of_admission=data['year_of_admission'],
            guardian_full_name=data['guardian_full_name'],
            guardian_contact=data['guardian_contact'],
            guardian_email=data['guardian_email'],
            user_id=user_id
        )

        db.session.add(new_application)
        db.session.commit()

        return jsonify({"message": f"Application created successfully with ID: {new_application.id}"}), 201

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400

    except KeyError as ke:
        logging.error(f"Missing required field: {ke.args[0]}")
        return jsonify({"error": f"Missing required field: {ke.args[0]}"}), 400

    except IntegrityError as ie:
        logging.error(f"IntegrityError: {ie}")
        db.session.rollback()
        return jsonify({"error": "IntegrityError occurred. Check database constraints."}), 500

    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({"error": str(e)}), 500

@application.route('/<int:application_id>', methods=['GET'])
def get_application(application_id):
    try:
        application = Application.query.get(application_id)
        if not application:
            return jsonify({"error": "Application not found in the database"}), 404

        application_data = {
            "id": application.id,
            "first_name": application.first_name,
            "last_name": application.last_name,
            "other_name": application.other_name,
            "date_of_birth": application.date_of_birth,
            "name_of_previous_school": application.name_of_previous_school,
            "previous_math_grade": application.previous_math_grade,
            "previous_english_grade": application.previous_english_grade,
            "current_level": application.current_level,
            "year_of_admission": application.year_of_admission,
            "guardian_full_name": application.guardian_full_name,
            "guardian_contact": application.guardian_contact,
            "guardian_email": application.guardian_email,
            "user_id": application.user_id
        }

        return jsonify({"application": application_data}), 200

    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({"error": "Internal server error"}), 500

@application.route('/<int:application_id>', methods=['PUT'])
def update_application(application_id):
    try:
        application = Application.query.get(application_id)
        if not application:
            return jsonify({"error": f"Application with ID {application_id} not found"}), 404

        data = request.json
        update_data = {field: data.get(field) for field in [
            'first_name', 'last_name', 'other_name', 'date_of_birth', 
            'name_of_previous_school', 'previous_math_grade', 'previous_english_grade', 
            'current_level', 'year_of_admission', 'guardian_full_name', 
            'guardian_contact', 'guardian_email']
        }

        for field, value in update_data.items():
            if value is not None:
                setattr(application, field, value)

        db.session.commit()

        return jsonify({"message": f"Application with ID {application_id} has been updated"}), 200

    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({"error": str(e)}), 500

@application.route('/<int:application_id>', methods=['DELETE'])
def delete_application(application_id):
    try:
        application = Application.query.get(application_id)
        if not application:
            return jsonify({"error": "Application not found"}), 404

        db.session.delete(application)
        db.session.commit()

        return jsonify({"message": "Application deleted successfully"}), 200

    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({"error": "Internal server error"}), 500