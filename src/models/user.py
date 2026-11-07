from dataclasses import dataclass

@dataclass
class User:
    # Модель пользователя системы
    user_id: int
    login: str
    password: str
    role_id: int
    fio: str | None = None
    contact: str | None = None
    address: str | None = None
