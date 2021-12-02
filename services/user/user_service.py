from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter


router = InferringRouter()


@cbv(router)
class User:
    from sqlalchemy.orm import Session
    from fastapi import Depends
    from services.database.database_service import get_db
    from services.database.schema.user_schema import UserSchema

    @router.get('/api/user/{user_id}', response_model=UserSchema)
    def get_user(self, user_id: str, db: Session = Depends(get_db)):
        from services.database.model.db_base_models import UserModel

        return UserModel.get_user_by_id(user_id, db)
