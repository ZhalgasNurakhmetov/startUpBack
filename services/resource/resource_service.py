from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter


router = InferringRouter()


@cbv(router)
class Resource:
    from services.database.schema.resource_schema import ResourceSchema, ResourceBaseSchema
    from services.auth.auth_service import get_current_user
    from services.database.schema.user_schema import UserSchema
    from fastapi import Depends
    from sqlalchemy.orm import Session
    from services.database.database_service import get_db

    @router.post('/api/resource/create', response_model=ResourceSchema)
    def create_resource(
            self,
            resource_info: ResourceBaseSchema,
            current_user: UserSchema = Depends(get_current_user),
            db: Session = Depends(get_db)
    ):
        import uuid
        from services.database.model.db_base_models import ResourceModel

        new_resource_id = str(uuid.uuid4())
        new_resource = ResourceModel(**resource_info.dict(), id=new_resource_id, ownerId=current_user.id, available=True)
        new_resource.save_to_db(db)
        return new_resource

    @router.put('/api/resource/edit/{resource_id}', response_model=ResourceSchema)
    def edit_resource(
            self,
            resource_id: str,
            resource_info: ResourceBaseSchema,
            current_user: UserSchema = Depends(get_current_user),
            db: Session = Depends(get_db)
    ):
        from services.database.model.db_base_models import ResourceModel
        from services.error_handler.error_handler_service import unauthorized_exception, resource_not_found_exception

        if not current_user:
            raise unauthorized_exception
        resource: ResourceModel = ResourceModel.get_resource_by_id(resource_id, db)
        if not resource:
            raise resource_not_found_exception
        resource.personal = resource_info.personal
        resource.title = resource_info.title
        resource.author = resource_info.author
        resource.year = resource_info.year
        resource.pageCount = resource_info.pageCount
        resource.literature = resource_info.literature
        resource.cover = resource_info.cover
        resource.language = resource_info.language
        resource.composition = resource_info.composition
        resource.format = resource_info.format
        resource.description = resource_info.description
        resource.condition = resource_info.condition
        resource.save_to_db(db)
        return resource

    @router.delete('/api/resource/delete/{resource_id}', response_model=ResourceSchema)
    def delete_resource(
            self,
            resource_id: str,
            current_user: UserSchema = Depends(get_current_user),
            db: Session = Depends(get_db)
    ):
        from services.error_handler.error_handler_service import unauthorized_exception, resource_not_found_exception
        from services.database.model.db_base_models import ResourceModel

        if not current_user:
            raise unauthorized_exception
        resource: ResourceModel = ResourceModel.get_resource_by_id(resource_id, db)
        if not resource:
            raise resource_not_found_exception
        resource.delete_from_db(db)
        return resource
