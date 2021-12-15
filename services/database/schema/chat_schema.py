from pydantic import BaseModel


class MessageCreateSchema(BaseModel):
    chatId: str
    userId: str
    message: str
    isRed: bool
    dateTime: str
