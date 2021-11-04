from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter


router = InferringRouter()


def get_db():
    from services.database.database_service import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@cbv(router)
class CurrentUser:
    from fastapi import Depends
    from services.database.schemas.user_schema import UserSchema
    from services.auth.auth_service import get_current_user

    @router.get('/api/user/me', response_model=UserSchema)
    def get_user(self, current_user: UserSchema = Depends(get_current_user)):
        return current_user
