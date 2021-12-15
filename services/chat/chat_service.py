from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class Chat:
    from typing import List
    from services.auth.auth_service import get_current_user
    from services.database.schema.user_schema import UserChatSchema, UserChatBaseSchema, UserSchema
    from sqlalchemy.orm import Session
    from services.database.database_service import get_db
    from fastapi import Depends

    @router.post('/api/chat/create/with/{second_user_id}', response_model=UserChatSchema)
    def create_one_to_one_chat(self, second_user_id: str, chat_info: UserChatBaseSchema, current_user: UserSchema = Depends(get_current_user), db: Session = Depends(get_db)):
        import uuid
        from services.database.model.db_base_models import ChatModel

        new_chat_id = str(uuid.uuid4())
        new_chat = ChatModel(id=new_chat_id, firstUserId=current_user.id, secondUserId=second_user_id, **chat_info.dict())
        new_chat.save_to_db(db)
        return new_chat

    @router.get('/api/chat/list', response_model=List[UserChatSchema])
    def get_chat_list(self, current_user: UserSchema = Depends(get_current_user), db: Session = Depends(get_db)):
        from services.database.model.db_base_models import ChatModel

        return ChatModel.get_all_chats(current_user.id, db)


class ConnectionManager:
    from starlette.websockets import WebSocket
    from typing import Any

    def __init__(self):
        from typing import Dict

        self.connections: Dict = {}

    async def connect(self, user_id: str, webSocket: WebSocket):
        await webSocket.accept()
        self.connections[user_id] = webSocket

    async def send_personal_message(self, message: Any, user_id: str, contact_id: str):
        # await self.connections[contact_id].send_json(message)
        await self.connections[user_id].send_json(message)
