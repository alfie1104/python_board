from pydantic import BaseModel, validator


class AnswerCreate(BaseModel):
    content: str

    # 빈 문자열을 허용하지 않도록 validator('content') 어노테이션을 적용한 not_empty 함수 추가
    # AsnwerCreate 스키마에 content값이 저장될 때 실행됨
    @validator("content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v
