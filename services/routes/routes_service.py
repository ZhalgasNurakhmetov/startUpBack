from services.current_user.current_user_service import router as CurrentUserServiceRouter
from services.auth.auth_service import router as AuthServiceRouter
from services.password.password_service import router as PasswordServiceRouter
from services.resource.resource_service import router as ResourceServiceRouter
from services.user_resource.user_resource_service import router as UserResourceRouter


def initialize_routes(app):
    app.include_router(AuthServiceRouter)
    app.include_router(CurrentUserServiceRouter)
    app.include_router(PasswordServiceRouter)
    app.include_router(ResourceServiceRouter)
    app.include_router(UserResourceRouter)
