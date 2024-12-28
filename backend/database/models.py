from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Hand(Base):
    __tablename__ = 'hands'
    id = Column(Integer, primary_key=True)
    hand_id = Column(String)
    pot = Column(Integer)
    winner = Column(String)

engine = create_engine('sqlite:///poker_tracker.db')
Base.metadata.create_all(engine)
