import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.utils import get_random_id
import requests
from vk.exceptions import VkAPIError
import json
from googletrans import Translator

token = '1aa70f3daf3610a84669b33954f8968ee7d6ff52cd383df18479ecee767d8ad60455a71845c9ddc5c26e3'

session = vk_api.VkApi(token=token, api_version='5.107')
vkapi = session.get_api()
longpoll = VkBotLongPoll(session, group_id=195861998, wait=25)

info = vkapi.groups.getLongPollServer(group_id=195861998)
server, key, ts = info['server'], info['key'], info['ts']

vkapi.groups.setLongPollSettings(group_id=195861998, message_new=1)

with open('keyboard.json', 'r', encoding='utf-8') as f:
    keyboard = json.dumps(json.load(f))

translator = Translator()

while True:

    long_poll_response = requests.get('{server}?act=a_check&key={key}&ts={ts}&wait=25'.format(server=server,
                                                                                    key=key, ts=ts)).json()
    if 'updates' not in long_poll_response:
        continue

    msg, user_id = '', ''

    try:
        for el in long_poll_response['updates']:
            user_id = el['object']['user_id']

            if el['type'] == 'message_new':
                if el['object']['out'] == 0:
                    if el['object']['body'] == 'Начать':
                        vkapi.messages.send(user_id=user_id, random_id=get_random_id(), peer_id=user_id,
                                            message='Привет, я могу рассказать тебе о погоде!')

                        result = translator.translate('Привет, я могу рассказать тебе о погоде!', src='ru', dest='en')
                        vkapi.messages.send(user_id=user_id, random_id=get_random_id(), peer_id=user_id,
                                            message=result.text)
                        vkapi.messages.send(user_id=user_id, random_id=get_random_id(), peer_id=user_id,
                                            message="Выберите действие",
                                            keyboard=keyboard)
                    # elif el['object']['body'] == 'Хочу узнать погоду':

                        # result = translator.translate(el['object']['body'], src='ru', dest='en')
                        # vkapi.messages.send(user_id=user_id, random_id=get_random_id(), peer_id=user_id,
                        #                     message=result.text)
    except VkAPIError:
        continue

    print(requests.get('{server}?act=a_check&key={key}&ts={ts}&wait=25'.format(server=server,
                                                                               key=key, ts=ts)).json())

    ts = long_poll_response['ts']

