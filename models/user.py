from pydantic import BaseModel


class User(BaseModel):
    id: str
    photo: str
    birthDate: str
    firstName: str
    lastName: str
    email: str
    password: str
    city: str
    about: str