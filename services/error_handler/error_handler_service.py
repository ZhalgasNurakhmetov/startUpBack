from fastapi import HTTPException, status


user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Пользователь не найден',
)

credentials_exception = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail='Неверный логин или пароль',
)

token_expired_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Время действия токена истекло",
)

unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Не авторизован",
    headers={"WWW-Authenticate": "Bearer"},
)

user_already_exist_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Учетная запись уже существует',
)

new_passwords_not_equal_exception = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Новые пароли не совпадают",
)

current_password_exception = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Неверный текущий пароль"
)
