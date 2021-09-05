import datetime as dt

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
from external_requests import CheckCityExisting, GetWeatherRequest
import models
import schemas
from schemas import RegisterUserRequest, UserModel

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/cities/', summary='Create City', response_model=schemas.City,
          description='Создание города по его названию', tags=['city'])
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    check = CheckCityExisting()
    if not check.check_existing(city.name):
        raise HTTPException(
            status_code=400,
            detail='Параметр city должен быть существующим городом')

    city_object = db.query(models.City).filter(
        models.City.name == city.name).first()
    if city_object is None:
        city_object = models.City(name=city.name)
        s = db
        s.add(city_object)
        s.commit()

    return {'id': city_object.id, 'name': city_object.name, 'weather': city_object.weather}


@app.post('/get-cities/', summary='Get Cities')
def cities_list(q: str = Query(description="Название города", default=None)):
    """
    Получение списка городов
    """
    cities = db.query(City).all()

    return [{'id': city.id, 'name': city.name, 'weather': city.weather} for city in cities]


@app.post('/users-list/', summary='')
def users_list():
    """
    Список пользователей
    """
    users = db.query(User).all()
    return [{
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'age': user.age,
    } for user in users]


@app.post('/register-user/', summary='CreateUser', response_model=UserModel)
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = db
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)


@app.get('/all-picnics/', summary='All Picnics', tags=['picnic'])
def all_picnics(datetime: dt.datetime = Query(default=None, description='Время пикника (по умолчанию не задано)'),
                past: bool = Query(default=True, description='Включая уже прошедшие пикники')):
    """
    Список всех пикников
    """
    picnics = db.query(Picnic)
    if datetime is not None:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())

    return [{
        'id': pic.id,
        'city': db.query(City).filter(City.id == pic.id).first().name,
        'time': pic.time,
        'users': [
            {
                'id': pr.user.id,
                'name': pr.user.name,
                'surname': pr.user.surname,
                'age': pr.user.age,
            }
            for pr in db.query(PicnicRegistration).filter(PicnicRegistration.picnic_id == pic.id)],
    } for pic in picnics]


@app.get('/picnic-add/', summary='Picnic Add', tags=['picnic'])
def picnic_add(city_id: int = None, datetime: dt.datetime = None):
    p = Picnic(city_id=city_id, time=datetime)
    s = db
    s.add(p)
    s.commit()

    return {
        'id': p.id,
        'city': db.query(City).filter(City.id == p.id).first().name,
        'time': p.time,
    }


@app.get('/picnic-register/', summary='Picnic Registration', tags=['picnic'])
def register_to_picnic(*_, **__,):
    """
    Регистрация пользователя на пикник
    (Этот эндпойнт необходимо реализовать в процессе выполнения тестового задания)
    """
    # TODO: Сделать логику
    return ...

