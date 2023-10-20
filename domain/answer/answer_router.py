from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud

router = APIRouter(prefix="/api/answer")


@router.post(
    "/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT
)  # 출력으로 response_model 대신 status_code를 사용하였음. 이렇게 함으로써 204 응답코드를 리턴하여 응답없음을 나타낼 수 있음
def answer_create(
    question_id: int,
    _answer_create: answer_schema.AnswerCreate,
    db: Session = Depends(get_db),
):
    # create answer
    question = question_crud.get_question(db, question_id=question_id)

    if not question:
        raise HTTPException(status_code=404, detail="Data not found")

    answer_crud.create_answer(db, question=question, answer_create=_answer_create)
