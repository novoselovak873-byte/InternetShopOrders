from repositories import user_repository
from models.user import User

def authenticate(login, password) -> User | None:
    # Аутентификация пользователя по логину и паролю
    user = user_repository.get_by_login(login)
    if user and user.password == password:
        return user
    return None

def register_client(login, password, fio, contact, address) -> int:
    # Валидация данных и регистрация нового клиента
    if not login.strip() or not password.strip():
        raise Exception("Логин и пароль не могут быть пустыми!")
    if user_repository.get_by_login(login):
        raise Exception("Пользователь с таким логином уже существует!")
    return user_repository.create(login, password, 2, fio, contact, address)
