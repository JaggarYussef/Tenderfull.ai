from sqlalchemy import Column, String, DateTime, Text, Integer, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
import os
import uuid

Base = declarative_base()

class Tender(Base):
    __tablename__ = 'tenders'
    
    id = Column(String, primary_key=True)
    posting_title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    publication_date = Column(DateTime, nullable=False)
    publication_language = Column(String(2), nullable=False)
    description_paragraph = Column(Text, nullable=False)
    status = Column(String(20), nullable=False)
    workspace_id = Column(String, nullable=False, default=str(uuid.uuid4()))

class UserInput(Base):
    __tablename__ = 'user_input'

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    email = Column(String, nullable=False)
    score = Column(Float, nullable=False)