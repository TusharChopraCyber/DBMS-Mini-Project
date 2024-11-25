from flask import jsonify, current_app
from flask_jwt_extended import create_access_token
from app.models.user import User
from app import db
import traceback

class AuthController:
    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        return jsonify({"error": "Invalid credentials"}), 401

    @staticmethod
    def create_admin(username, password, admin_key, email):
        try:
            if admin_key != current_app.config['ADMIN_CREATION_KEY']:
                return jsonify({"error": "Invalid admin creation key"}), 403

            if not User.is_valid_du_email(email):
                return jsonify({"error": "Invalid email domain. Must be a .du.ac.in email"}), 400

            if User.query.filter_by(username=username).first():
                return jsonify({"error": "Username already exists"}), 400

            if User.query.filter_by(email=email).first():
                return jsonify({"error": "Email already registered"}), 400

            user = User(
                username=username,
                email=email,
                is_admin=True
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            return jsonify({"message": "Admin user created successfully"}), 201
            
        except Exception as e:
            db.session.rollback()
            print(traceback.format_exc())
            return jsonify({
                "error": "Could not create admin user",
                "details": str(e)
            }), 500

    @staticmethod
    def create_user(username, password, exam_roll_no, email):
        try:
            # Validate email domain
            if not User.is_valid_du_email(email):
                return jsonify({"error": "Invalid email domain. Must be a .du.ac.in email"}), 400

            # Check if username already exists
            if User.query.filter_by(username=username).first():
                return jsonify({"error": "Username already exists"}), 400

            # Check if email already exists
            if User.query.filter_by(email=email).first():
                return jsonify({"error": "Email already registered"}), 400

            # Check if exam_roll_no is already registered
            if User.query.filter_by(exam_roll_no=exam_roll_no).first():
                return jsonify({"error": "Exam roll number already registered"}), 400

            user = User(
                username=username,
                email=email,
                exam_roll_no=exam_roll_no,
                is_admin=False
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            return jsonify({"message": "User created successfully"}), 201
            
        except Exception as e:
            db.session.rollback()
            print(traceback.format_exc())
            return jsonify({
                "error": "Could not create user",
                "details": str(e)
            }), 500