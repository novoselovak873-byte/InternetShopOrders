from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    login: str
    password: str
    role_id: int
    last_name: str | None = None
    first_name: str | None = None
    patronymic: str | None = None
    contact: str | None = None
    address: str | None = None
