from pydantic import BaseModel


class PasswordResetRequestSchema(BaseModel):
    username: str


class NewPasswordSchema(BaseModel):
    newPassword: str
    newPasswordConfirm: str


class ChangePasswordSchema(NewPasswordSchema):
    oldPassword: str
