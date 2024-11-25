from app import db
from app.models.result import Result

class ResultController:
    @staticmethod
    def get_result(exam_roll_no):
        result = Result.query.filter_by(exam_roll_no=exam_roll_no).first()
        if result:
            return {
                'exam_roll_no': result.exam_roll_no,
                'student_name': result.student_name,
                'marks': result.marks,
                'grade': result.grade
            }
        return None

    @staticmethod
    def create_result(data):
        result = Result(
            exam_roll_no=data['exam_roll_no'],
            student_name=data['student_name'],
            marks=data['marks'],
            grade=data['grade']
        )
        db.session.add(result)
        db.session.commit()
        return result 