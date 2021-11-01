from services.user.user_registration.user_registration_service import router as UserRegistrationRouter


def initialize_routes(app):
    app.include_router(UserRegistrationRouter)
