from sqlalchemy.orm import sessionmaker
from database.models import engine

Session = sessionmaker(bind=engine)
session = Session()
