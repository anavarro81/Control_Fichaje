import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")


# Se crea la configuracion para desarrollo.
class DevelopmentConfig(Config):
    DEBUG = True
    # Parametros de conexion con la BBDD.
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_USER = os.environ.get("MYSQL_USER")
    # MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_PASSWORD = ""
    MYSQL_DB = os.environ.get("MYSQL_DB")


config = {"development": DevelopmentConfig}
