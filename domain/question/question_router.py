from fastapi import APIRouter

# from database import SessionLocal
from database import get_db
from models import Question

router = APIRouter(prefix="/api/question")


# @router.get("/list")
# def question_list():
#     db = SessionLocal()  # db 세션 생성
#     _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#     db.close()  # 사용한 세션을 커넥션풀에 반환 (세션을 종료하는것이 아님)
#     return _question_list


# get_db를 이용하여 세션 생성 및 반환하도록 개선 수정
@router.get("/list")
def question_list():
    with get_db() as db:  # db 세션 생성 및 사용완료시 반환(db.close()가 실행됨)
        _question_list = db.query(Question).order_by(Question.create_date.desc()).all()

    return _question_list
