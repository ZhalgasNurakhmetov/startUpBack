from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from services.database.database_service import SessionLocal
from services.database.models.db_base_models import UserModel
from services.database.schemas.user_schema import UserSchema

router = InferringRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@cbv(router)
class UserGet:

    @router.get('/api/user/{user_id}', response_model=UserSchema)
    def register_user(self, user_id: str, db: Session = Depends(get_db)):
        return db.query(UserModel).filter(UserModel.id == user_id).first()
