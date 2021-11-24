from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class CurrentUser:
    from services.database.database_service import get_db
    from sqlalchemy.orm import Session
    from services.database.schema.user_schema import UserCreateSchema, UserSchema, UserEditSchema
    from fastapi import Depends
    from services.auth.auth_service import get_current_user
    from services.database.model.db_base_models import UserModel

    @router.post('/api/current_user/registration', response_model=UserSchema)
    def create_user(self, user: UserCreateSchema, db: Session = Depends(get_db)):
        from services.database.model.db_base_models import UserModel
        from services.auth.auth_service import pwd_context
        from services.error_handler.error_handler_service import user_already_exist_exception
        import uuid
        from services.mail.mail_service import Mail

        user.username = user.username.lower()
        if UserModel.get_user_by_username(user.username, db):
            raise user_already_exist_exception
        new_user_id = str(uuid.uuid4())
        user.password = pwd_context.hash(user.password)
        new_user = UserModel(**user.dict(), id=new_user_id)
        new_user.save_to_db(db)
        Mail.send_email(
            user.username,
            '[Bookberry] Добро пожаловать!',
            '''Теперь Вы можете добавить книги, которыми Вы готовы поделиться и которые Вы хотели бы получить!
                \nНайдите людей со схожими интересами'''
        )
        return new_user

    @router.get('/api/current_user/me', response_model=UserSchema)
    def get_current_user(self, current_user: UserSchema = Depends(get_current_user)):
        return current_user

    @router.put('/api/current_user/edit', response_model=UserSchema)
    def edit_user(
            self,
            user_info: UserEditSchema,
            current_user: UserModel = Depends(get_current_user),
            db: Session = Depends(get_db)
    ):
        current_user.firstName = user_info.firstName
        current_user.lastName = user_info.lastName
        current_user.city = user_info.city
        current_user.birthDate = user_info.birthDate
        current_user.about = user_info.about
        current_user.save_to_db(db)
        return current_user


@cbv(router)
class UserContact:
    from services.auth.auth_service import get_current_user
    from services.database.model.db_base_models import UserModel
    from fastapi import Depends
    from sqlalchemy.orm import Session
    from services.database.database_service import get_db
    from services.database.schema.user_schema import UserSchema

    @router.post('/api/user/follow/{user_id}', response_model=UserSchema)
    def follow_user(
            self,
            user_id: str,
            current_user: UserModel = Depends(get_current_user),
            db: Session = Depends(get_db)
    ):
        from services.database.model.db_base_models import UserModel

        user: UserModel = UserModel.get_user_by_id(user_id, db)
        current_user.following.append(user)
        current_user.save_to_db(db)
        return current_user

    @router.post('/api/user/unfollow/{user_id}', response_model=UserSchema)
    def unfollow_user(
            self, user_id: str,
            current_user: UserModel = Depends(get_current_user),
            db: Session = Depends(get_db)
    ):
        from services.database.model.db_base_models import UserModel

        user: UserModel = UserModel.get_user_by_id(user_id, db)
        current_user.following.remove(user)
        current_user.save_to_db(db)
        return current_user

