from services.current_user.current_user_service import router as CurrentUserServiceRouter
from services.auth.auth_service import router as AuthServiceRouter
from services.password.password_service import router as PasswordServiceRouter
from services.resource.resource_service import router as ResourceServiceRouter
from services.user_resource.user_resource_service import router as UserResourceRouter
from services.user.user_service import router as UserServiceRouter
from services.chat.chat_service import router as ChatServiceRouter
from services.photo.photo_service import router as PhotoServiceRouter
from services.image.image_service import router as ImageServiceRouter


def initialize_routes(app):
    app.include_router(AuthServiceRouter)
    app.include_router(CurrentUserServiceRouter)
    app.include_router(PasswordServiceRouter)
    app.include_router(ResourceServiceRouter)
    app.include_router(UserResourceRouter)
    app.include_router(UserServiceRouter)
    app.include_router(ChatServiceRouter)
    app.include_router(PhotoServiceRouter)
    app.include_router(ImageServiceRouter)
