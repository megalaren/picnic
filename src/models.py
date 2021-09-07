from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from database import Base
from external_requests import GetWeatherRequest


class City(Base):
    """
    Город
    """
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    @property
    def weather(self) -> str:
        """
        Возвращает текущую погоду в этом городе
        """
        r = GetWeatherRequest()
        weather = r.get_weather(self.name)
        return weather

    def __repr__(self):
        return f'<Город "{self.name}">'


class User(Base):
    """
    Пользователь
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    age = Column(Integer, nullable=True)

    __table_args__ = (UniqueConstraint(
        'name', 'surname', 'age', name='unique user'),)

    def __repr__(self):
        return f'<Пользователь {self.surname} {self.name}>'


class Picnic(Base):
    """
    Пикник
    """
    __tablename__ = 'picnic'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    time = Column(DateTime, nullable=False)

    city_object = relationship('City', backref='picnics')

    @property
    def city(self) -> str:
        return self.city_object.name

    __table_args__ = (UniqueConstraint(
        'city_id', 'time', name='unique picnic'),)

    def __repr__(self):
        return f'<Пикник {self.id}>'


class PicnicRegistration(Base):
    """
    Регистрация пользователя на пикник
    """
    __tablename__ = 'picnic_registration'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    picnic_id = Column(Integer, ForeignKey('picnic.id'), nullable=False)

    user = relationship('User', backref='picnics')
    picnic = relationship('Picnic', backref='users')

    __table_args__ = (UniqueConstraint(
        'user_id', 'picnic_id', name='unique registration'),)

    def __repr__(self):
        return f'<Регистрация {self.id}>'
