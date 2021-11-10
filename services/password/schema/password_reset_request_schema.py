from pydantic import BaseModel


class PasswordResetSchema(BaseModel):
    username: str


class NewPasswordSchema(BaseModel):
    newPassword: str
    newPasswordConfirm: str


class ChangePasswordSchema(NewPasswordSchema):
    oldPassword: str
