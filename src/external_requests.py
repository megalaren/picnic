import requests

from settings import WEATHER_URL


class Weather:
    """
    Выполняет запрос на получение текущей погоды для города
    """
    def __init__(self):
        """
        Инициализирует класс
        """
        self.session = requests.Session()

    def get_weather_url(self, city):
        """
        Генерирует url включая в него необходимые параметры
        Args:
            city: Город
        Returns:
            str
        """
        return WEATHER_URL.format(city=city)

    def send_request(self, url):
        """
        Отправляет запрос на сервер
        Args:
            url: Адрес запроса
        Returns:
            'requests.Response' object or None
        """
        try:
            response = self.session.get(url)
        except Exception:
            return None
        return response

    def get_weather(self, city):
        """
        Делает запрос на получение погоды, возвращает температуру
        Args:
            city: Город
        Returns:
            str
        """
        url = self.get_weather_url(city)
        response = self.send_request(url)
        if response is None or response.status_code != 200:
            return None
        # если поменялась схема api сервиса погоды, то вернём None:
        main = response.json().get('main')
        if not main:
            return None
        return main.get('temp')

    def check_existing(self, city):
        """
        Проверяет наличие города
        Args:
            city: Название города
        Returns:
            bool, str
        """
        url = self.get_weather_url(city)
        response = self.send_request(url)
        if response is None:
            return False, 'Отсутствует соединение с интернетом'
        if response.status_code == 200:
            return True, 'Ок'
        if response.status_code == 404:
            return False, 'Параметр city должен быть существующим городом'
        return False, 'Произошла неизвестная ошибка'
