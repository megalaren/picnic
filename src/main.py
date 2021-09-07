import datetime as dt

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List

from database import engine, SessionLocal, Base
from external_requests import Weather
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/cities/', response_model=schemas.City, summary='Create City',
          tags=['cities'])
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    """
    Создание города по его названию
    """
    is_existing, detail = Weather().check_existing(city.name)
    if not is_existing:
        raise HTTPException(
            status_code=400,
            detail=detail)

    city_object = db.query(models.City).filter(
        models.City.name == city.name).first()
    if city_object is None:
        city_object = models.City(name=city.name)
        db.add(city_object)
        db.commit()
        db.refresh(city_object)
    return city_object


@app.get('/cities/', response_model=List[schemas.City], summary='Get Cities',
         tags=['cities'])
def read_cities(q: str = Query(description='Название города', default=None),
                db: Session = Depends(get_db)):
    """
    Получение списка городов
    """
    cities = db.query(models.City)
    if q:
        cities = cities.filter(models.City.name == q)
    return cities.all()


@app.post('/users/', response_model=schemas.User, summary='Create User',
          tags=['users'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация пользователя
    """
    user_object = db.query(models.User).filter(
        models.User.name == user.name,
        models.User.surname == user.surname,
        models.User.age == user.age
    ).first()
    if user_object is None:
        user_object = models.User(**user.dict())
        db.add(user_object)
        db.commit()
        db.refresh(user_object)
    return user_object


@app.get('/users/', response_model=List[schemas.User], summary='Get Users',
         tags=['users'])
def read_users(
        min_age: int = Query(description='Минимальный возраст', default=None),
        max_age: int = Query(description='Максимальный возраст', default=None),
        db: Session = Depends(get_db)):
    """
    Получение списка пользователей
    """
    users = db.query(models.User)
    if min_age:
        users = users.filter(models.User.age >= min_age)
    if max_age:
        users = users.filter(models.User.age <= max_age)
    return users.all()


@app.post('/picnics/', response_model=schemas.Picnic, summary='Add Picnic',
          tags=['picnics'])
def picnic_add(picnic: schemas.PicnicCreate, db: Session = Depends(get_db)):
    """
    Создание пикника
    """
    # Проверим наличие города с таким id в базе
    city_id = picnic.city_id
    city_obj = db.query(models.City).filter(models.City.id == city_id).first()
    if city_obj is None:
        raise HTTPException(
            status_code=404, detail=f'City with id = {city_id} not found')

    picnic_object = db.query(models.Picnic).filter(
        models.Picnic.city_id == city_id,
        models.Picnic.time == picnic.time
    ).first()
    if picnic_object is None:
        picnic_object = models.Picnic(**picnic.dict())
        db.add(picnic_object)
        db.commit()
        db.refresh(picnic_object)
    return picnic_object


@app.get('/picnics/', response_model=List[schemas.Picnic],
         summary='Get Picnics', tags=['picnics'])
def read_picnics(
        datetime: dt.datetime = Query(
            default=None,
            description='Время пикника (по умолчанию не задано)'),
        past: bool = Query(
            default=True,
            description='Включая уже прошедшие пикники'),
        db: Session = Depends(get_db)):
    """
    Получение списка всех пикников
    """
    picnics = db.query(models.Picnic).options(
        joinedload(models.Picnic.users).options(
            joinedload(models.PicnicRegistration.user)),
        joinedload(models.Picnic.city_object))

    if datetime is not None:
        picnics = picnics.filter(models.Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(models.Picnic.time >= dt.datetime.now())

    return [{
        'id': pic.id,
        'city': pic.city,
        'time': pic.time,
        'users': [
            {
                'id': pr.user.id,
                'name': pr.user.name,
                'surname': pr.user.surname,
                'age': pr.user.age,
            } for pr in pic.users],
    } for pic in picnics]


@app.post('/picnics/register/', response_model=schemas.PicnicRegistration,
          summary='Picnic Registration', tags=['picnics'])
def register_to_picnic(picnic_reg: schemas.PicnicRegistration,
                       db: Session = Depends(get_db)):
    """
    Регистрация пользователя на пикник
    """
    # Проверим наличие пикника и пользователя с такими id в базе
    user_id = picnic_reg.user_id
    picnic_id = picnic_reg.picnic_id
    user_obj = db.query(models.User).filter(models.User.id == user_id).first()
    if user_obj is None:
        raise HTTPException(
            status_code=404, detail=f'User with id = {user_id} not found')
    picnic_obj = db.query(models.Picnic).filter(
        models.Picnic.id == picnic_id).first()
    if picnic_obj is None:
        raise HTTPException(
            status_code=404, detail=f'Picnic with id = {picnic_id} not found')

    picnic_reg_obj = db.query(models.PicnicRegistration).filter(
        models.PicnicRegistration.user_id == user_id,
        models.PicnicRegistration.picnic_id == picnic_id,
    ).first()
    if picnic_reg_obj is None:
        picnic_reg_obj = models.PicnicRegistration(**picnic_reg.dict())
        db.add(picnic_reg_obj)
        db.commit()
        db.refresh(picnic_reg_obj)
    return picnic_reg_obj
