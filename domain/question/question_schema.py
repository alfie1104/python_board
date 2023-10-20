import datetime

from pydantic import BaseModel
from domain.answer.answer_schema import Answer


# API의 입출력을 validation하기 위한 pydantic용 스키마인 Question 스키마 선언
# 만약 content를 출력항목에서 제외하고 싶다면 (DB에는 그대로 유지) Question 스키마에서 content를 제외하면 됨(DB Model은 건드릴 필요 없음)
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []

    class Config:  # Question Model의 값을 자동으로 Question 스키마로 매핑하기 위해 orm_mode = True 적용
        orm_mode = True
