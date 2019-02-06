from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_string = "postgresql://localhost:5432/web_int"

engine = create_engine(db_string)
Base = declarative_base()


class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    data = Column(JSONB)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()
