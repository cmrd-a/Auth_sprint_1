from sqlalchemy import create_engine

from Auth.config import config

engine = create_engine(config.pg_url)
# SessionLocal = sessionmaker(bind=engine)
