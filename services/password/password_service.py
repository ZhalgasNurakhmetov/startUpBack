from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter


router = InferringRouter()


@cbv(router)
class PasswordReset:
    from services.database.database_service import get_db
    from sqlalchemy.orm import Session
    from fastapi import Depends
    from services.password.schema.password_reset_request_schema import PasswordResetRequestSchema
    from fastapi import Request

    @router.post('/api/password/reset')
    def password_reset_request(self,  user_credential: PasswordResetRequestSchema, request: Request, db: Session = Depends(get_db)):
        from services.database.models.db_base_models import UserModel
        from services.auth.auth_service import generate_access_token
        from datetime import timedelta
        from services.error_handler.error_handler_service import user_not_found_exception

        user_credential.username = user_credential.username.lower()
        try:
            user: UserModel = UserModel.get_user_by_username(user_credential.username, db)
        except Exception:
            raise user_not_found_exception
        access_token_expires = timedelta(minutes=15)
        token = generate_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
        self.send_gmail(user.username, token['access_token'], request.client.host)

    @staticmethod
    def send_gmail(recipient_email: str, token: str, host: str):
        from settings.settings import settings
        from email.message import EmailMessage
        import smtplib

        gmail_user = settings.MAIL_USERNAME
        gmail_password = settings.MAIL_PASSWORD
        message = EmailMessage()
        body = '''С вашего аккаунта был отправлен запрос на восстановление пароля.
                \nЕсли Вы не отправляли запрос, игнорируйте данное сообщение!
                \nДля восстановления пароля пройдите по ссылке\n{}:8000/api/password/reset/{}'''.format(host, token)
        message.set_content(body)
        message['Subject'] = '[Bookberry] Восстановление пароля!'
        message['From'] = gmail_user
        message['To'] = recipient_email
        server = smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(message)
        server.close()


@cbv(router)
class NewPasswordSetForm:
    from fastapi.responses import HTMLResponse
    from fastapi import Request
    from services.password.schema.password_reset_request_schema import NewPasswordSchema
    from services.database.database_service import get_db
    from sqlalchemy.orm import Session
    from fastapi import Depends

    @router.get('/api/password/reset/{token}', response_class=HTMLResponse)
    def get_reset_password_form(self, request: Request, token: str):
        from starlette.templating import Jinja2Templates

        templates = Jinja2Templates(directory="templates")
        return templates.TemplateResponse('password_reset.html', {
            'request': request,
            'token': token,
        })

    @router.post('/api/password/reset/{token}', response_class=HTMLResponse)
    def reset_password(self, request: Request, token: str, new_password_info: NewPasswordSchema, db: Session = Depends(get_db)):
        from jose import jwt, JWTError
        from settings.settings import settings
        from datetime import datetime
        from services.error_handler.error_handler_service import new_passwords_not_equal_exception
        from services.auth.auth_schema import TokenData
        from services.auth.auth_service import get_user_by_id
        from services.auth.auth_service import pwd_context
        from starlette.templating import Jinja2Templates
        from services.database.models.db_base_models import UserModel
        from services.error_handler.error_handler_service import user_not_found_exception, unauthorized_exception

        if not new_password_info.newPassword == new_password_info.newPasswordConfirm:
            raise new_passwords_not_equal_exception

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("sub")
            expires: datetime = payload.get("exp")
            if user_id is None:
                raise user_not_found_exception
            if expires is None or datetime.utcnow() > datetime.fromtimestamp(expires):
                raise unauthorized_exception
            token_data = TokenData(id=user_id, expires=expires)
        except JWTError:
            raise unauthorized_exception
        user: UserModel = get_user_by_id(token_data.id, db)
        if user is None:
            raise user_not_found_exception
        user.password = pwd_context.hash(new_password_info.newPassword)
        user.save_to_db(db)

        # TODO works in postman, in browser something is wrong
        templates = Jinja2Templates(directory="templates")
        # return templates.TemplateResponse('reset_password_final.html', {
        #     'request': request,
        # })


@cbv(router)
class PasswordChange:
    from services.password.schema.password_reset_request_schema import ChangePasswordSchema
    from services.auth.auth_service import get_current_user
    from fastapi import Depends
    from services.database.models.db_base_models import UserModel
    from sqlalchemy.orm import Session
    from services.database.database_service import get_db
    from services.database.schemas.user_schema import UserSchema

    @router.post('/api/password/change', response_model=UserSchema)
    def change_password(self, change_password_info: ChangePasswordSchema, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
        from services.error_handler.error_handler_service import new_passwords_not_equal_exception
        from services.auth.auth_service import pwd_context
        from services.error_handler.error_handler_service import current_password_exception

        if not pwd_context.verify(change_password_info.oldPassword, current_user.password):
            raise current_password_exception
        if not change_password_info.newPassword == change_password_info.newPasswordConfirm:
            raise new_passwords_not_equal_exception
        current_user.password = pwd_context.hash(change_password_info.newPassword)
        current_user.save_to_db(db)
        return current_user



