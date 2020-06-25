import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import requests
from vk.exceptions import VkAPIError
import json
from googletrans import Translator
import weather


def send_message(message):
    user_id = ''

    for element in long_poll_response['updates']:
        user_id = element['object']['user_id']

    vkapi.messages.send(user_id=user_id, random_id=get_random_id(), peer_id=user_id,
                        message=message)


def send_keyboard():
    user_id = ''

    for element in long_poll_response['updates']:
        user_id = element['object']['user_id']

    vkapi.messages.send(user_id=user_id, random_id=get_random_id(), peer_id=user_id,
                        message='Привет, я могу рассказать тебе о погоде!', keyboard=keyboard)


with open('keyboard.json', 'r', encoding='utf-8') as f:
    keyboard = json.dumps(json.load(f))

token = '1aa70f3daf3610a84669b33954f8968ee7d6ff52cd383df18479ecee767d8ad60455a71845c9ddc5c26e3'
session = vk_api.VkApi(token=token, api_version='5.107')
vkapi = session.get_api()
longpoll = VkBotLongPoll(session, group_id=195861998, wait=25)
longpoll_info = vkapi.groups.getLongPollServer(group_id=195861998)
server, key, ts = longpoll_info['server'], longpoll_info['key'], longpoll_info['ts']
vkapi.groups.setLongPollSettings(group_id=195861998, message_new=1)

translator = Translator()

isWeather = False
isDate = False
isDateSent = False
city_name = ''
forecast_date = ''

while True:

    long_poll_response = requests.get('{server}?act=a_check&key={key}&ts={ts}&wait=25'.format(server=server,
                                                                                              key=key, ts=ts)).json()

    print(requests.get('{server}?act=a_check&key={key}&ts={ts}&wait=25'.format(server=server,
                                                                               key=key, ts=ts)).json())

    if 'updates' not in long_poll_response:
        continue

    try:
        for el in long_poll_response['updates']:
            if el['type'] != 'message_new' or el['object']['out'] != 0:
                continue

            if el['object']['body'] == 'Начать':
                send_keyboard()

            elif el['object']['body'] == 'Хочу узнать погоду!':
                send_message('Введите название города, в котором хотите узнать погоду')
                isWeather = True

            elif isWeather is True:
                city_name = el['object']['body']

                print(city_name)
                city_name = translator.translate(city_name, src='ru', dest='en').text
                print(city_name)
                isWeather = False
                isDate = True

            elif isDateSent is True:
                forecast_date = el['object']['body']

                print(forecast_date)
                weather = weather.get_weather(city_name=city_name, forecast_date=forecast_date)
                send_message(weather)
                isWeather = False
                isDate = False
                isDateSent = False
                city_name = ''
                forecast_date = ''

        if isDate is True:
            send_message('Введите дату прогноза в формате гггг мм дд')
            isDate = False
            isDateSent = True

    except VkAPIError:
        continue

    ts = long_poll_response['ts']

