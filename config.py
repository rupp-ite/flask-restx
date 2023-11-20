import os
class Config:
    def __init__(self):
        project_root = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(project_root,'data', 'data.db')
        self.DEBUG = True
        self.SQLALCHEMY_DATABASE_URI = f'sqlite:///{database_path}'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.JWT_SECRET_KEY = 'my-secret'
        