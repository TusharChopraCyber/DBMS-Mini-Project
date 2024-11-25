from app import db
from datetime import datetime

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_roll_no = db.Column(db.BigInteger, unique=True, nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 