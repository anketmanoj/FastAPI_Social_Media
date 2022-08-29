from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    hashedPassword = pwd_context.hash(password)
    return hashedPassword

def verify(plainPassword: str, hashedPassword: str):
    return pwd_context.verify(plainPassword, hashedPassword)