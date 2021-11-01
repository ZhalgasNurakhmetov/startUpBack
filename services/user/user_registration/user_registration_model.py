from pydantic import BaseModel


class UserRegistrationModel(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str
    birthDate: str
    city: str
