from services.user.current_user_service import router as CurrentUserServiceRouter
from services.auth.auth_service import router as AuthServiceRouter
from services.password.password_service import router as PasswordServiceRouter


def initialize_routes(app):
    app.include_router(AuthServiceRouter)
    app.include_router(CurrentUserServiceRouter)
    app.include_router(PasswordServiceRouter)
