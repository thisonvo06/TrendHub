import bcrypt

# 密码加密（bcrypt 自带加盐，无需 passlib）
def get_password_hash(password: str):
    pwd_bytes = password.encode('utf-8')
    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode('utf-8')

# 密码校验
def verify_password(password: str, password_hash: str):
    return bcrypt.checkpw(
        password.encode('utf-8'),
        password_hash.encode('utf-8')
    )
