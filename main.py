import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import requests
from random import randint as rnd
from vk.exceptions import VkAPIError
import json
from vk_api import bot_longpoll

token = '1aa70f3daf3610a84669b33954f8968ee7d6ff52cd383df18479ecee767d8ad60455a71845c9ddc5c26e3'

session = vk_api.VkApi(token=token)
vkapi = session.get_api()
longpoll = VkBotLongPoll(session, group_id=195861998, wait=25)

# session = vk_api.auth(access_token=token)
# vkapi = vk.API(session, v="5.107")

info = vkapi.groups.getLongPollServer(group_id=195861998)
server = info['server']
key = info['key']
ts = info['ts']

vkapi.groups.setLongPollSettings(group_id=195861998, message_new=1)

with open('keyboard.json', 'r', encoding='utf-8') as f:
    keyboard = json.dumps(json.load(f))

while True:

    response = requests.get('{server}?act=a_check&key={key}&ts={ts}&wait=25'.format(server=server,
                                                                                    key=key, ts=ts)).json()
    if 'updates' not in response:
        continue

    msg = ''
    user_id = ''

    try:
        for el in response['updates']:
            user_id = el['object']['user_id']

            if el['type'] == 'message_new':
                if el['object']['out'] == 0:
                    if el['object']['body'] == 'Начать':
                        vkapi.messages.send(user_id=user_id, random_id=get_random_id(), peer_id=user_id,
                                            message='Привет, я могу рассказать тебе о погоде!')

                        vkapi.messages.send(user_id=user_id, random_id=rnd(1, 2 ** 63), peer_id=user_id,
                                            message="Выберите действие",
                                keyboard=keyboard)
    except VkAPIError:
        continue

    print(requests.get('{server}?act=a_check&key={key}&ts={ts}&wait=25'.format(server=server,
                                                                               key=key, ts=ts)).json())
    ts = str(int(ts) + 1)

