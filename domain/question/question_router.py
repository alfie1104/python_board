from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# from database import SessionLocal
from database import get_db
from domain.question import question_schema, question_crud
from models import Question

router = APIRouter(prefix="/api/question")


# @router.get("/list")
# def question_list():
#     db = SessionLocal()  # db 세션 생성
#     _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#     db.close()  # 사용한 세션을 커넥션풀에 반환 (세션을 종료하는것이 아님)
#     return _question_list


# # get_db를 이용하여 세션 생성 및 반환하도록 개선 수정
# @router.get("/list")
# def question_list():
#     with get_db() as db:  # db 세션 생성 및 사용완료시 반환(db.close()가 실행됨)
#         _question_list = db.query(Question).order_by(Question.create_date.desc()).all()

#     return _question_list


"""
 [FastAPI의 Depends를 사용하여 with문 사용시 보다 편리하게 개선]
 get_db함수를 with문과 쓰지 않고, question_list함수의 매개변수로 db객체를 주입받았음. db: Session은 db객체가 Session 타입임을 의미
 이때 get_db 함수에 자동으로 contextmanager가 적용되기 때문에 (Depends에서 contextmanager를 적용하게끔 설계되어 있음)
 database.py의 get_db함수에 적용했던 @contextlib.contextmanager 어노테이션을 제거해야함
"""


# @router.get("/list")
@router.get("/list", response_model=list[question_schema.Question])  # pydantic 스키마 적용
def question_list(db: Session = Depends(get_db)):
    _question_list = question_crud.get_question_list(db)

    return _question_list


@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id)
    return question
