from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter


router = InferringRouter()


@cbv(router)
class UserResource:
    from sqlalchemy.orm import Session
    from fastapi import Depends
    from services.database.database_service import get_db

    @router.post('/api/user/{user_id}/like/{resource_id}')
    def like_resource(self, user_id: str, resource_id: str, db: Session = Depends(get_db)):
        import uuid
        from services.database.model.db_base_models import ResourceLikeModel, ResourceModel

        new_resource_like_id = str(uuid.uuid4())
        new_resource_like = ResourceLikeModel(id=new_resource_like_id, user_id=user_id, resource_id=resource_id)
        resource: ResourceModel = ResourceModel.get_resource_by_id(resource_id, db)
        resource.likes = resource.likes + 1
        new_resource_like.save_to_db(db)
        resource.save_to_db(db)
        return

    @router.delete('/api/user/{user_id}/unlike/{resource_id}')
    def unlike_resource(self, user_id: str, resource_id: str, db: Session = Depends(get_db)):
        from services.database.model.db_base_models import ResourceLikeModel, ResourceModel

        resource_like: ResourceLikeModel = ResourceLikeModel.get_like_by_id(user_id, resource_id, db)
        resource: ResourceModel = ResourceModel.get_resource_by_id(resource_id, db)
        resource.likes = resource.likes - 1
        resource_like.delete_from_db(db)
        resource.save_to_db(db)
        return
