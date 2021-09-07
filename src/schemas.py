from datetime import datetime
from typing import List

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str


class CityCreate(CityBase):
    pass


class City(CityBase):
    """Формирует тело ответа из БД."""
    id: int
    weather: float

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    surname: str
    age: int


class UserCreate(UserBase):
    pass


class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

    class Config:
        orm_mode = True


class PicnicBase(BaseModel):
    time: datetime


class PicnicCreate(PicnicBase):
    city_id: int


class Picnic(BaseModel):
    id: int
    city: str  # метод city() в models.Picnic, возвращает название города
    time: datetime
    users: List[User]

    class Config:
        orm_mode = True


class PicnicRegistration(BaseModel):
    user_id: int
    picnic_id: int

    class Config:
        orm_mode = True
