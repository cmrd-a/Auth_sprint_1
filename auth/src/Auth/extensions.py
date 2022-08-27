from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
redis_client = FlaskRedis()
