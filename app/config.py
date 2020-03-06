class DebugConfig:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(DebugConfig):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
