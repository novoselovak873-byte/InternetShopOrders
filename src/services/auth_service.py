from repositories import user_repository
from models.user import User

def authenticate(login, password) -> User | None:
    user = user_repository.get_by_login(login)
    if user and user.password == password:
        return user
    return None

def register_client(login, password, last_name, first_name, patronymic, contact, address) -> int:
    if not login.strip() or not password.strip():
        raise Exception("Логин и пароль не могут быть пустыми!")
    if not last_name.strip() or not first_name.strip():
        raise Exception("Фамилия и Имя являются обязательными!")
    if user_repository.get_by_login(login):
        raise Exception("Пользователь с таким логином уже существует!")
    return user_repository.create(login, password, 2, last_name, first_name, patronymic, contact, address)
