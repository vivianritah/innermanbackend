from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from school_api.models.admissions import Admissions
from school_api.models.user import User
from school_api.extensions import db

admissions_bp = Blueprint('admissions', __name__, url_prefix='/api/v1/admissions')

@admissions_bp.route('/', methods=['GET'])
def get_admissions():
    admissions = Admissions.query.all()
    admissions_list = [{
        'class': admission.class_name,
        'fees': {
            'day': admission.tuition_day,
            'boarding': admission.tuition_boarding,
            'registration': admission.registration_fees,
            'uniformBoarding': admission.uniform_boarding,
            'uniformDay': admission.uniform_day
        }
    } for admission in admissions]
    return jsonify(admissions_list), 200


@admissions_bp.route('/', methods=['POST'])
@jwt_required()
def create_admission():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user.isadmin:
        return jsonify({'message': 'Unauthorized access'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        class_name = data['class']
        fees = data['fees']
        tuition_day = fees['day']
        tuition_boarding = fees['boarding']
        registration_fees = fees['registration']
        uniform_boarding = fees.get('uniformBoarding')
        uniform_day = fees.get('uniformDay')

        new_admission = Admissions(
            class_name=class_name,
            tuition_day=tuition_day,
            tuition_boarding=tuition_boarding,
            registration_fees=registration_fees,
            uniform_boarding=uniform_boarding,
            uniform_day=uniform_day
        )
        db.session.add(new_admission)
        db.session.commit()
        return jsonify({'message': 'Admission fees added successfully'}), 201

    except KeyError as e:
        return jsonify({'message': f'Missing key: {e}'}), 400


@admissions_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_admission(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user.isadmin:
        return jsonify({'message': 'Unauthorized access'}), 401

    admission = Admissions.query.get(id)
    if not admission:
        return jsonify({'message': 'Admission fees not found'}), 404

    data = request.get_json()

    try:
        admission.class_name = data['class']  # Update class_name
        admission.tuition_day = data['fees']['day']
        admission.tuition_boarding = data['fees']['boarding']
        admission.registration_fees = data['fees']['registration']
        admission.uniform_boarding = data['fees'].get('uniformBoarding')
        admission.uniform_day = data['fees'].get('uniformDay')

        db.session.commit()
        return jsonify({'message': 'Admission fees updated successfully'}), 200

    except KeyError as e:
        return jsonify({'message': f'Missing key: {e}'}), 400
    except Exception as e:
        return jsonify({'message': f'An error occurred: {e}'}), 500




@admissions_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_admission(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user.isadmin:
        return jsonify({'message': 'Unauthorized access'}), 401

    admission = Admissions.query.get(id)
    if not admission:
        return jsonify({'message': 'Admission fees not found'}), 404

    db.session.delete(admission)
    db.session.commit()
    return jsonify({'message': 'Admission fees deleted successfully'}), 200
