import datetime
from pydantic import BaseModel, validator
from domain.user.user_schema import User


class AnswerCreate(BaseModel):
    content: str

    # 빈 문자열을 허용하지 않도록 validator('content') 어노테이션을 적용한 not_empty 함수 추가
    # AsnwerCreate 스키마에 content값이 저장될 때 실행됨
    @validator("content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v


class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None
    question_id: int

    class Config:
        orm_mode = True  # DB 모델의 속성을 스키마에 매핑하기 위해 orm_mode를 True로 설정


class AnswerUpdate(Answer):
    answer_id: int
