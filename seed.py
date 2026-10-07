from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.environment import DATABASE_URL
from data.user_data import user_list
from models.base import Base


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    db.add_all(user_list)
    db.commit()
finally:
    db.close()
