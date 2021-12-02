from typing import List, Optional

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
        resource_info.title = resource_info.title.strip()
        resource_info.author = resource_info.author.strip()
        if resource_info.year:
            resource_info.year = resource_info.year.strip()
        if resource_info.description:
            resource_info.description = resource_info.description.strip()
        if resource_info.pageCount:
            resource_info.pageCount = resource_info.pageCount.strip()
        new_resource = ResourceModel(**resource_info.dict(), id=new_resource_id, ownerId=current_user.id,
                                     available=True)
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
        resource.title = resource_info.title.strip()
        resource.author = resource_info.author.strip()
        if resource_info.year:
            resource_info.year = resource_info.year.strip()
        if resource_info.pageCount:
            resource_info.pageCount = resource_info.pageCount.strip()
        resource.literature = resource_info.literature
        resource.cover = resource_info.cover
        resource.language = resource_info.language
        resource.composition = resource_info.composition
        resource.format = resource_info.format
        if resource_info.description:
            resource_info.description = resource_info.description.strip()
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
        for like in resource.favoriteUserList:
            like.delete_from_db(db)
        resource.delete_from_db(db)
        return resource


@cbv(router)
class ResourceSearch:
    from services.database.schema.resource_schema import ResourceSchema
    from fastapi import Depends
    from sqlalchemy.orm import Session
    from services.database.database_service import get_db
    from services.auth.auth_service import get_current_user
    from services.database.schema.user_schema import UserSchema

    @router.get('/api/resource/search', response_model=List[ResourceSchema])
    def get_resource_by_search(
            self,
            searchText: Optional[str],
            criteria: Optional[str],
            literature: Optional[str] = '',
            language: Optional[str] = '',
            composition: Optional[str] = '',
            db: Session = Depends(get_db),
            current_user: UserSchema = Depends(get_current_user),
    ):
        from services.database.model.db_base_models import ResourceModel

        resource_list: List[ResourceModel] = ResourceModel.get_non_personal_resource_list(
            current_user.id,
            criteria,
            searchText.strip(),
            db
        )

        resource_list = [resource for resource in resource_list if resource.owner.city == current_user.city]

        if literature != '':
            resource_list = [resource for resource in resource_list if resource.literature == literature]
        if language != '':
            resource_list = [resource for resource in resource_list if resource.language == language]
        if composition != '':
            resource_list = [resource for resource in resource_list if resource.composition == composition]
        return resource_list


@cbv(router)
class ResourceAvailability:
    from services.database.schema.resource_schema import ResourceSchema
    from fastapi import Depends
    from services.auth.auth_service import get_current_user
    from sqlalchemy.orm import Session
    from services.database.database_service import get_db

    @router.put('/api/resource/{resource_id}/available', response_model=ResourceSchema)
    def set_resource_available(
            self,
            resource_id: str,
            _ = Depends(get_current_user),
            db: Session = Depends(get_db)):
        from services.database.model.db_base_models import ResourceModel

        resource: ResourceModel = ResourceModel.get_resource_by_id(resource_id, db)
        resource.available = not resource.available
        resource.save_to_db(db)
        return resource
