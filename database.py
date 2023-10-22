# import contextlib

from sqlalchemy import create_engine, MetaData
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

# SQLite 데이터베이스로 ORM을 사용할때 발생하는 문제점 해결을 위해 아래 naming_convention을 Base.metadata에 적용
# index, unique key, primary key등에 대한 규칙을 새롭게 설정하였음(데이터베이스에서 디폴트값으로 명명되던 이름을 수동으로 설정한 것)
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
Base.metadata = MetaData(naming_convention=naming_convention)


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
