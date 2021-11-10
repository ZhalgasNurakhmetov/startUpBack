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
    from jose import jwt, JWTError
    from settings.settings import settings
    from services.auth.schema.auth_schema import TokenDataSchema
    from datetime import datetime
    from services.error_handler.error_handler_service import user_not_found_exception, unauthorized_exception

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        expires: datetime = payload.get("exp")
        if user_id is None:
            raise user_not_found_exception
        if expires is None or datetime.utcnow() > datetime.fromtimestamp(expires):
            raise unauthorized_exception
        token_data = TokenDataSchema(id=user_id, expires=expires)
    except JWTError:
        raise unauthorized_exception
    user = get_user_by_id(token_data.id, db)
    if user is None:
        raise user_not_found_exception
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
    from services.database.model.db_base_models import UserModel

    return UserModel.get_user_by_id(user_id, db)


@cbv(router)
class Auth:
    from services.auth.schema.auth_schema import TokenSchema
    from services.auth.schema.auth_schema import UserCredentialsSchema

    @router.post('/auth', response_model=TokenSchema)
    def authenticate(self, credentials: UserCredentialsSchema, db: Session = Depends(get_db)):
        from datetime import timedelta
        from settings.settings import settings

        user = self.authenticate_user(credentials, db)
        access_token_expires = timedelta(weeks=settings.ACCESS_TOKEN_EXPIRE_WEEKS)
        return generate_access_token(data={"sub": user.id}, expires_delta=access_token_expires)

    @staticmethod
    def authenticate_user(credentials: UserCredentialsSchema, db: Session):
        from services.database.model.db_base_models import UserModel
        from services.error_handler.error_handler_service import user_not_found_exception, credentials_exception

        try:
            user: UserModel = Auth.get_user_by_username(credentials.username, db)
        except Exception:
            raise user_not_found_exception
        if not pwd_context.verify(credentials.password, user.password):
            raise credentials_exception
        return user

    @staticmethod
    def get_user_by_username(username: str, db: Session):
        from services.database.model.db_base_models import UserModel

        return UserModel.get_user_by_username(username, db)
