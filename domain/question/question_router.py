from fastapi import APIRouter

from database import SessionLocal
from models import Question

router = APIRouter(prefix="/api/question")


@router.get("/list")
def question_list():
    db = SessionLocal()  # db 세션 생성
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    db.close()  # 사용한 세션을 커넥션풀에 반환 (세션을 종료하는것이 아님)
    return _question_list
