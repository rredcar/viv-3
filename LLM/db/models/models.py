from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, UniqueConstraint, SMALLINT, DATETIME, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship



Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(VARCHAR(255), nullable=False)
    password = Column(VARCHAR(300), nullable=False)
    email = Column(VARCHAR(255), nullable=True)

    __table_args__ = (
        UniqueConstraint('username', name='uq_username'),
        UniqueConstraint('email', name='uq_email'),
    )

class MusicalComposition(Base):
    __tablename__ = 'musical_compositions'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    url = Column(VARCHAR(255), nullable=False)

    user = relationship('User', backref='musical_compositions')
















