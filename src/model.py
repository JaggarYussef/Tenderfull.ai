from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserQuery(Base):
    __tablename__ = 'user_queries'

    id = Column(Integer, primary_key=True)
    query = Column(Text, nullable=False)
    email = Column(String(255), nullable=False)
    score = Column(Float, nullable=False)

    def __repr__(self):
        return f"<UserQuery(id={self.id}, email='{self.email}', score={self.score})>"