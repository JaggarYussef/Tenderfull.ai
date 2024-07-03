from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from model import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base

import  os



PG_HOST="postgres"
PG_USER="airflow"
PG_PASSWORD="airflow"
PG_DB="airflow"
PG_PORT=5432

app = FastAPI()


class UserInputCreate(BaseModel):
    query: str
    email: str
    score: float

DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'

print(DATABASE_URI)
engine = create_engine(DATABASE_URI)

class UserInput(Base):
    __tablename__ = 'user_input'

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    email = Column(String, nullable=False)
    score = Column(Float, nullable=False)
Base.metadata.create_all(engine)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful")
except SQLAlchemyError as e:
    print(f"Database connection failed: {str(e)}")

Session = sessionmaker(bind=engine)

def insert_user_input(query: str, email: str, score: float):
    session = Session()
    try:
        new_input = UserInput(query=query, email=email, score=score)
        session.add(new_input)
        session.commit()
        print(f"Successfully inserted new row with id: {new_input.id}")
        return new_input.id
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/user_input/")
async def create_user_input(user_input: UserInputCreate):
    try:
        new_id = insert_user_input(user_input.query, user_input.email, user_input.score)
        if new_id is not None:
            return {"id": new_id, "message": "User input created successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to create user input: Unknown error")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")