# import contextlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./myapi.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)  # create_engine은 커넥션 풀을 생성함

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # 데이터베이스에 접속하기 위해 필요한 클래스

Base = declarative_base()  # 반환된 Base는 데이터 베이스 모델을 구성할 때 활용함


"""
[get_db]
 참고 : contextmanager  -> https://docs.python.org/ko/3/library/contextlib.html
 db 세션 객체를 리턴하는 제너레이터(이터레이터를 생성해주는 함수)인 get_db 함수
 제너레이터 함수에 @contextlib.contextmanager 어노테이션을 적용했으므로 다음과 같이 with문과 함께 쓸 수 있음

 with get_db() as db:
   # db 세션 객체를 사용

 with문을 벗어나는 순간 get_db 함수의 finally에 작성한 db.close() 함수가 자동으로 실행됨
"""


# @contextlib.contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
