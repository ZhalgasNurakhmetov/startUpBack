from services.user.user_get_service import router as UserGetRouter
from services.user.user_registration_service import router as UserRegistrationRouter
from services.auth.auth_service import router as AuthServiceRouter


def initialize_routes(app):
    app.include_router(UserRegistrationRouter)
    app.include_router(UserGetRouter)
    app.include_router(AuthServiceRouter)
