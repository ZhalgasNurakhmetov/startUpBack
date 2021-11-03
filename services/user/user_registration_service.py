from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from passlib.context import CryptContext

router = InferringRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@cbv(router)
class UserRegistration:
    from services.database.database_service import get_db
    from sqlalchemy.orm import Session
    from services.database.schemas.user_schema import UserCreateSchema, UserSchema
    from fastapi import Depends

    @router.post('/api/user/registration', response_model=UserSchema)
    def register_user(self, user: UserCreateSchema, db: Session = Depends(get_db)):
        from services.database.models.db_base_models import UserModel

        from fastapi import HTTPException
        import uuid

        user.username = user.username.lower()
        if UserModel.get_user_by_username(user.username, db):
            raise HTTPException(status_code=409, detail='Учетная запись уже существует')
        new_user_id = str(uuid.uuid4())
        user.password = pwd_context.hash(user.password)
        new_user = UserModel(**user.dict(), id=new_user_id)
        new_user.save_to_db(db)
        self.send_gmail(user.username)
        return new_user

    @staticmethod
    def send_gmail(recipient_email: str):
        from settings.settings import settings
        from email.message import EmailMessage
        import smtplib

        gmail_user = settings.MAIL_USERNAME
        gmail_password = settings.MAIL_PASSWORD
        message = EmailMessage()
        body = '''Теперь Вы можете добавить книги, которыми Вы готовы поделиться и которые Вы хотели бы получить!.
                \nНайдите людей со схожими интересами!'''
        message.set_content(body)
        message['Subject'] = '[Bookberry] Добро пожаловать!'
        message['From'] = gmail_user
        message['To'] = recipient_email
        server = smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(message)
        server.close()
