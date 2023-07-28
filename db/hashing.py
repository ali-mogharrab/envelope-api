from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

class Hash:
    @staticmethod
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(hashed_password, plained_password):
        return pwd_cxt.verify(plained_password, hashed_password)
