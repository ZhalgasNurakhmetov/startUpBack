import os

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

path = os.getcwd()
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}
PHOTOS_FOLDER = os.path.join(path, 'saved', 'images')


def allowed_file(fileType: str):
    return '/' in fileType and fileType.split('/')[1].lower() in ALLOWED_EXTENSIONS


router = InferringRouter()


@cbv(router)
class Image:
    from services.database.schema.resource_schema import ResourceSchema
    from fastapi import Depends, File, UploadFile
    from sqlalchemy.orm import Session
    from services.database.database_service import get_db
    from starlette.responses import FileResponse

    @router.post('/api/image/upload/{resource_id}', response_model=ResourceSchema)
    def upload_image(self, resource_id: str, image: UploadFile = File(...), db: Session = Depends(get_db)):
        from services.error_handler.error_handler_service import invalid_file_extension_exception
        import shutil
        from services.database.model.db_base_models import ResourceModel

        if not allowed_file(image.content_type):
            raise invalid_file_extension_exception
        image_path = 'saved/images/{}'.format(resource_id)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        resource: ResourceModel = ResourceModel.get_resource_by_id(resource_id, db)
        resource.imagePath = '/{}'.format(image_path)
        resource.save_to_db(db)
        return resource

    @router.get('/saved/images/{resource_id}', response_class=FileResponse)
    def display_image(self, resource_id: str):
        return 'saved/images/{}'.format(resource_id)
