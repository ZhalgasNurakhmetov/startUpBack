import os

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

path = os.getcwd()
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}
PHOTOS_FOLDER = os.path.join(path, 'saved', 'photos')


def allowed_file(fileType: str):
    return '/' in fileType and fileType.split('/')[1].lower() in ALLOWED_EXTENSIONS


router = InferringRouter()


@cbv(router)
class Photo:
    from fastapi import Depends, File, UploadFile
    from sqlalchemy.orm import Session
    from starlette.responses import FileResponse
    from services.auth.auth_service import get_current_user
    from services.database.database_service import get_db
    from services.database.model.db_base_models import UserModel
    from services.database.schema.user_schema import UserSchema

    @router.post('/api/photo/upload', response_model=UserSchema)
    def upload_photo(self, photo: UploadFile = File(...), current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
        import shutil
        from typing import List
        from services.database.model.db_base_models import ChatModel
        from services.error_handler.error_handler_service import invalid_file_extension_exception

        if not allowed_file(photo.content_type):
            raise invalid_file_extension_exception

        photo_path = 'saved/photos/{}'.format(current_user.id)
        with open(photo_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        current_user.photoPath = '/{}'.format(photo_path)
        chats: List[ChatModel] = ChatModel.get_all_chats(current_user.id, db)
        for chat in chats:
            if chat.firstUserId == current_user.id:
                chat.firstUserPhotoPath = '/{}'.format(photo_path)
            else:
                chat.secondUserPhotoPath = '/{}'.format(photo_path)
            chat.save_to_db(db)
        current_user.save_to_db(db)
        return current_user

    @router.get('/saved/photos/{user_id}', response_class=FileResponse)
    def display_photo(self, user_id: str):
        return 'saved/photos/{}'.format(user_id)
