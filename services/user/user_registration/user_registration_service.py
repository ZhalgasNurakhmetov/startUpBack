from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from services.user.user_registration.user_registration_model import UserRegistrationModel

router = InferringRouter()


@cbv(router)
class UserRegistration:

    @router.post('/api/user/registration')
    def register_user(self, user: UserRegistrationModel):
        return user.dict()
