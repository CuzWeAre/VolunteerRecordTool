import bcrypt


class UserAuth:
    """用于用户验证的类"""

    # def __init__(self, username='', passwd=''):
    #     """初始化"""
    #     self.hashed_password = None
    #     self.password = passwd
    #     self.username = username
    #     self.hashed_passwd = ''
    #     self.salt = ''

    @staticmethod
    def hashpw(password):
        """用于对密码哈希化的类"""
        if password == '':
            raise ValueError("Password cannot be empty")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password, salt

    @staticmethod
    def auth(input_password, salt_store, hashed_password_store):
        hashed_password = bcrypt.hashpw(input_password, salt_store)
        return bcrypt.checkpw(hashed_password_store, hashed_password)
