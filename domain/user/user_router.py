from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "b9238b705df439aaa0a4f36027992075b82989bf60b79db8b5244b285028fb2e"  # 터미널에서 openssl rand -hex 32로 생성
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(prefix="/api/user")


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다."
        )

    user_crud.create_user(db, user_create=_user_create)


@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # check user and password
    user = user_crud.get_user(db, username=form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        # 사용자가 없거나 비밀번호가 일치하지 않을 경우 401 오류 반환
        # 401오류는 사용자 인증 오류로, 보통 401 오류를 반환할때는 인증 방식에 대한 추가 정보인 WWW-Authenticate항목도 헤더 정보에 포함하여 리턴함
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(data, SECRET_KEY, ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
    }


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    # 매개변수인 token은 FastAPI의 security 패키지에 있는 OAuth2PasswordBearer에 의해 자동 매핑됨
    # OAuth2PasswordBearer(tokenUrl="/api/user/login")에서 사용한 tokenUrl은 로그인 API의 URL을 의미함
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user
