from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import re

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    exam_roll_no = db.Column(db.BigInteger, unique=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def is_valid_du_email(email):
        # Check if email ends with .du.ac.in
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.du\.ac\.in$'
        return bool(re.match(pattern, email)) 