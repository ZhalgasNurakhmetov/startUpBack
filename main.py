from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket

from services.chat.chat_service import ConnectionManager
from services.database.database_service import engine, Base, get_db
from services.routes.routes_service import initialize_routes

Base.metadata.create_all(engine, checkfirst=True)

app = FastAPI(title="Bookberry server", version="0.1.0")

webSocket_manager = ConnectionManager()
webSocket_read_manager = ConnectionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_routes(app)


@app.websocket("/ws/{user_id}")
async def webSocket_endpoint(webSocket: WebSocket, user_id: str, db: Session = Depends(get_db)):
    import uuid
    from services.database.model.db_base_models import MessageModel

    await webSocket_manager.connect(user_id, webSocket)
    while True:
        message = await webSocket.receive_json()
        contact_id = message['contactId']
        del message['contactId']
        new_message_id = str(uuid.uuid4())
        new_message = MessageModel(id=new_message_id, **message)
        new_message.save_to_db(db)
        await webSocket_manager.send_personal_message(new_message.json(), user_id, contact_id)


@app.websocket("/ws/read_message/{user_id}")
async def webSocket_read_message(webSocket: WebSocket, user_id: str, db: Session = Depends(get_db)):
    from services.database.model.db_base_models import MessageModel

    await webSocket_read_manager.connect(user_id, webSocket)
    while True:
        req = await webSocket.receive_json()
        messages: List[MessageModel] = MessageModel.get_messages_by_chat_id(req['chatId'], db)
        for message in messages:
            if message.userId != req['userId']:
                message.isRed = True
                message.save_to_db(db)
        await webSocket_read_manager.read_message(req['contactId'])
