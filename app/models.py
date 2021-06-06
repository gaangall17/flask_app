from flask_login import UserMixin
from .sql_service import get_user

class UserData:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

class UserModel(UserMixin):
    def __init__(self, user_data):
        """
        :param user_data: UserData
        """

        self.id = user_data.username
        self.password = user_data.password
        self.email = user_data.email
    
    @staticmethod
    def query(username):
        user_doc = get_user(username)
        user_data = UserData(
            username=user_doc.username,
            password=user_doc.password,
            email=user_doc.email  
        )
        return UserModel(user_data)

        