from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta

from services.database.database_service import get_db

router = InferringRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from fastapi import HTTPException, status
    from jose import jwt, JWTError
    from settings.settings import settings
    from services.auth.auth_schema import TokenData
    from datetime import datetime

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не авторизован",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_expired_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Время действия токена истекло",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        expires: datetime = payload.get("exp")
        if user_id is None:
            raise credentials_exception
        if expires is None or datetime.utcnow() > expires:
            raise token_expired_exception
        token_data = TokenData(id=user_id, expires=expires)
    except JWTError:
        raise credentials_exception
    user = get_user_by_id(token_data.id, db)
    if user is None:
        raise credentials_exception
    return user


def generate_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    from datetime import datetime
    from jose import jwt
    from settings.settings import settings

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}


def get_user_by_id(user_id: str, db: Session):
    from services.database.models.db_base_models import UserModel

    return UserModel.get_user_by_id(user_id, db)


@cbv(router)
class Auth:
    from services.auth.auth_schema import Token
    from services.auth.auth_schema import UserCredentials

    @router.post('/auth', response_model=Token)
    def authenticate(self, credentials: UserCredentials, db: Session = Depends(get_db)):
        from datetime import timedelta
        from settings.settings import settings

        user = self.authenticate_user(credentials, db)
        access_token_expires = timedelta(weeks=settings.ACCESS_TOKEN_EXPIRE_WEEKS)
        return generate_access_token(data={"sub": user.id}, expires_delta=access_token_expires)

    @staticmethod
    def authenticate_user(credentials: UserCredentials, db: Session):
        from fastapi import HTTPException, status
        from services.database.models.db_base_models import UserModel

        try:
            user: UserModel = Auth.get_user_by_username(credentials.username, db)
        except Exception:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
        if not pwd_context.verify(credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Неверный логин или пароль')
        return user

    @staticmethod
    def get_user_by_username(username: str, db: Session):
        from services.database.models.db_base_models import UserModel

        return UserModel.get_user_by_username(username, db)
