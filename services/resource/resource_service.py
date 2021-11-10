from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter


router = InferringRouter()


@cbv(router)
class Resource:

    @router.post('/api/resource/create')
    def create_resource(self):
        pass

    @router.put('/api/resource/edit/{resource_id}')
    def edit_resource(self):
        pass

    @router.delete('/api/resource/delete/{resource_id}')
    def delete_resource(self):
        pass
