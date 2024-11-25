from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.result_controller import ResultController
from app.controllers.auth_controller import AuthController
from app.models.user import User

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    required_fields = ['username', 'password', 'exam_roll_no', 'email']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
        
    return AuthController.create_user(
        data['username'],
        data['password'],
        data['exam_roll_no'],
        data['email']
    )

@bp.route('/admin/signup', methods=['POST'])
def create_admin():
    data = request.get_json()
    
    required_fields = ['username', 'password', 'admin_key', 'email']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
        
    return AuthController.create_admin(
        data['username'],
        data['password'],
        data['admin_key'],
        data['email']
    )

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return AuthController.login(data['username'], data['password'])

@bp.route('/results/<int:exam_roll_no>', methods=['GET'])
@jwt_required()
def get_result(exam_roll_no):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # Allow admin to view any result
    if not user.is_admin:
        # Regular users can only view their own result
        if user.exam_roll_no != exam_roll_no:
            return jsonify({"error": "Unauthorized to view this result"}), 403

    result = ResultController.get_result(exam_roll_no)
    if result:
        return jsonify(result)
    return jsonify({"message": "Result awaited"}), 404

@bp.route('/results', methods=['POST'])
@jwt_required()
def create_result():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    data = request.get_json()
    result = ResultController.create_result(data)
    return jsonify({
        "message": "Result created successfully",
        "exam_roll_no": result.exam_roll_no
    }), 201 