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


class RegisterUserRequest(BaseModel):
    # принимает данные. Должен называться UserBase
    name: str
    surname: str
    age: int


class UserModel(BaseModel):
    # возврат данных. Надо назвать User и наследовать от UserBase
    id: int
    name: str
    surname: str
    age: int

    class Config:
        orm_mode = True
