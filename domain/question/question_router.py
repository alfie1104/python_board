from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status


# from database import SessionLocal
from database import get_db
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
from models import User

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
@router.get("/list", response_model=question_schema.QuestionList)  # pydantic 스키마 적용
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10):
    total, _question_list = question_crud.get_question_list(
        db, skip=page * size, limit=size
    )

    return {"total": total, "question_list": _question_list}


@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id)
    return question


# /create 라우터의 경우 응답할 내용이 없으므로 응답코드 204를 리턴하여 "응답 없음"을 표시
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(
    _question_create: question_schema.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    question_crud.create_question(
        db=db, question_create=_question_create, user=current_user
    )


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(
    _question_update: question_schema.QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_question = question_crud.get_question(
        db, question_id=_question_update.question_id
    )

    if db_question is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다."
        )

    if current_user.id != db_question.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="수정 권한이 없습니다."
        )
    question_crud.update_question(
        db=db, db_question=db_question, question_update=_question_update
    )


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(
    _question_delete: question_schema.QuestionDelete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_question = question_crud.get_question(
        db, question_id=_question_delete.question_id
    )

    if not db_question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다."
        )
    if current_user.id != db_question.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다."
        )
    question_crud.delete_question(db=db, db_question=db_question)
