from flask import Blueprint, jsonify, request
from core.models.assignments import Assignment
from core import db
from core.apis import decorators
from core.models import users, principals

principal_blueprint = Blueprint('principal', __name__)


@principal_blueprint.route('/principal/assignments', methods=['GET'])
@decorators.authenticate_principal
def get_principal_assignments(principal):
    if request.method == 'GET':
        custom_header = request.headers.get('X-Principal')
        print(f"Principal: {principal}")  # Add this line
        assignments_data = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
        print(f"Assignments Data: {assignments_data}")  # Add this line
        return jsonify({'data': [assignment.to_dict() for assignment in assignments_data]}), 200




@principal_blueprint.route('/principal/assignments/grade', methods=['POST'])
@decorators.accept_payload
@decorators.authenticate_principal
def grade_or_regrade_assignment(principal, incoming_payload):
    custom_header = request.headers.get('X-Principal')
    data = incoming_payload
    assignment_id = data.get('id')
    grade = data.get('grade')
    if not assignment_id or not grade:
        return jsonify({'error': 'Assignment ID and grade are required'}), 400
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
    assignment.grade = grade
    assignment.state = 'GRADED'
    db.session.commit()
    return jsonify({'data': assignment.to_dict()}), 200