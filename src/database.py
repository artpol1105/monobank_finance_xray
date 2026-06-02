import os
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(String, primary_key=True)
    time = Column(DateTime, nullable=False)
    description = Column(String)
    mcc = Column(Integer)
    amount = Column(Float)
    balance = Column(Float)
    cashbackAmount = Column(Float)
    category = Column(String)

DATABASE_URL = os.getenv("POSTGRES_URL")

if not DATABASE_URL:
    raise ValueError("Error: POSTGRES_URL hasn`t found in .env")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
    print("Database PostgreSQL successfully initialized! Table transactions created.")

if __name__ == "__main__":
    init_db()