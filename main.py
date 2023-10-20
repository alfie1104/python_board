from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.question import question_router
from domain.answer import answer_router

""" 
[참고 : https://wikidocs.net/175967]
아래 코드를 통해 FastAPI실행 시 필요한 테이블을 모두 생성할 수 있으나

 import models
 from database import engine
 models.Base.metadata.create_all(bind=engine)

데이터 베이스에 테이블이 존재하지 않을 경우에만 테이블을 생성하며,
한번 생성된 테이블에 대한 변경관리를 할 수 없기때문에 이 방법 대신
alembic을 사용하여 데이터베이스를 관리함.

1) alembic 설치 : pip install alembic

2) alembic 초기화 : alembic init migrations
 - migrations 디렉토리와 alembic.ini파일이 생성됨
 - migrations 디렉토리 : alembic 도구를 사용할 때 생성되는 리비전 파일을 저장하는 용도
 - alembic.ini : alembic의 환경설정 파일

3) alembic.ini 파일 수정
 - sqlalchemy.url = 적합한 url 입력(예 : sqlite 사용시, sqlalchemy.url = sqlite:///./myapi.db)

4) migrations 디렉토리의 env.py 파일 수정
 - import models 추가
 - target_metadata = None => target_metadata = models.Base.metadata 로 수정

5) 리비전 파일 생성 : alembic revision --autogenerate
 - migrations/versions 디렉토리에 fed28bf52b05_.py와 같은 리비전 파일이 생성됨
 - 리비전 파일에는 테이블을 생성 또는 변경하는 실행문이 들어있음

6) 리비전 파일 실행 : alembic upgrade head
 - 테이블이 생성됨 (예 : SQLite 사용 시, db명.db 파일 생성됨)
"""

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello")
def hello():
    return {"message": "Overall Spec."}


app.include_router(question_router.router)  # question_router.py파일의 router 객체를 app객체에 등록
app.include_router(answer_router.router)
