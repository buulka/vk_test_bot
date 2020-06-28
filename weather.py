import requests
from googletrans import Translator


def get_weather(city_name, forecast_date):
    try:
        url = 'https://www.metaweather.com/'
        eng_city_name = str(city_name)
        eng_city_name = eng_city_name.lower()

        woeid = requests.get(url + 'api/location/search/?query=' + eng_city_name).json()

        forecast_date = forecast_date.lstrip()
        forecast_date = forecast_date.rstrip()
        forecast_date = forecast_date.replace(' ', '/')

        weather = requests.get(url + 'api/location/' + str(woeid[0]['woeid']) + '/' + forecast_date + '/').json()

        forecast = weather[0]

        translator = Translator()

        weather_state_name = str(translator.translate(forecast['weather_state_name'], src='en', dest='ru').text)

        forecast_to_return = 'Состояние погоды: ' + weather_state_name + '\n' \
                             + 'Мин. температура: ' + str(round(forecast['min_temp'], 1)) + '°C' + '\n' \
                             + 'Макс. температура: ' + str(round(forecast['max_temp'], 1)) + '°C' + '\n ' \
                             + 'Средняя температура: ' + str(round(forecast['the_temp'], 1)) + '°C' + '\n' \
                             + 'Скорость ветра: ' + str(round(forecast['wind_speed'] / 2.237, 1)) + ' м/c' + '\n' \
                             + 'Направление ветра: ' + str(round(forecast['wind_direction'], 1)) + '°' + '\n' \
                             + 'Давление: ' + str(round(forecast['air_pressure'] / 1.333, 1)) + ' мм рт ст' + '\n' \
                             + 'Влажность: ' + str(round(forecast['humidity'], 1)) + ' %' + '\n' \
                             + 'Видимость: ' + str(round(forecast['visibility'] * 1.609, 1)) + ' км' + '\n'

        return forecast_to_return

    except:
        return 'Упс:( Не знаю погоду в этом городе либо за эту дату'
