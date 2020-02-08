class DebugConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(DebugConfig):
    DEBUG = False
