from passlib.context import CryptContext


CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def check_password(password: str, password_hash: str) -> bool:
    return CRIPTO.verify(password, password_hash)

def create_password_hash(password: str) -> str:
    return CRIPTO.hash(password)
