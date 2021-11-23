from fastapi import Form
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from services.auth.auth_service import check_token

router = InferringRouter()


@cbv(router)
class Password:
    from services.password.schema.password_schema import PasswordResetSchema
    from fastapi.responses import HTMLResponse
    from fastapi import Request
    from services.password.schema.password_schema import ChangePasswordSchema
    from services.auth.auth_service import get_current_user
    from fastapi import Depends
    from services.database.model.db_base_models import UserModel
    from sqlalchemy.orm import Session
    from services.database.database_service import get_db
    from services.database.schema.user_schema import UserSchema

    @router.post('/api/password/reset')
    def reset_password(self, user_credential: PasswordResetSchema, request: Request, db: Session = Depends(get_db)):
        from services.database.model.db_base_models import UserModel
        from services.auth.auth_service import generate_access_token
        from datetime import timedelta
        from services.error_handler.error_handler_service import user_not_found_exception
        from services.mail.mail_service import Mail

        user_credential.username = user_credential.username.lower()
        try:
            user: UserModel = UserModel.get_user_by_username(user_credential.username, db)
        except Exception:
            raise user_not_found_exception
        access_token_expires = timedelta(minutes=15)
        token = generate_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
        Mail.send_email(
            user.username,
            '[Bookberry] Восстановление пароля!',
            '''С вашего аккаунта был отправлен запрос на восстановление пароля.
                \nЕсли Вы не отправляли запрос, игнорируйте данное сообщение!
                \nДля восстановления пароля пройдите по ссылке\n{}:8000/api/password/reset/{}'''
                .format(request.client.host, token['access_token'])
        )

    @router.get('/api/password/reset/{token}', response_class=HTMLResponse)
    def get_reset_password_form(self, request: Request, token: str):
        from starlette.templating import Jinja2Templates

        templates = Jinja2Templates(directory="templates")
        return templates.TemplateResponse('password_reset.html', {
            'request': request,
            'token': token,
        })

    @router.post('/api/password/reset/{token}', response_class=HTMLResponse)
    def reset_password_by_token(
            self,
            request: Request,
            token: str,
            newPassword: str = Form(...), newPasswordConfirm: str = Form(...),
            db: Session = Depends(get_db)
    ):
        from services.error_handler.error_handler_service import new_passwords_not_equal_exception
        from services.auth.auth_service import pwd_context
        from starlette.templating import Jinja2Templates
        from services.database.model.db_base_models import UserModel

        if not newPassword == newPasswordConfirm:
            raise new_passwords_not_equal_exception
        user: UserModel = check_token(token, db)
        user.password = pwd_context.hash(newPassword)
        user.save_to_db(db)

        templates = Jinja2Templates(directory="templates")
        return templates.TemplateResponse('reset_password_final.html', {
            'request': request,
        })

    @router.post('/api/password/change', response_model=UserSchema)
    def change_password(
            self,
            change_password_info: ChangePasswordSchema,
            current_user: UserModel = Depends(get_current_user),
            db: Session = Depends(get_db)
    ):
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
