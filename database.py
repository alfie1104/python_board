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
