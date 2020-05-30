import vk
import requests
from random import randint as rnd
from vk.exceptions import VkAPIError

token = '1aa70f3daf3610a84669b33954f8968ee7d6ff52cd383df18479ecee767d8ad60455a71845c9ddc5c26e3'

session = vk.AuthSession(access_token=token)
vkapi = vk.API(session, v="5.107")

info = vkapi.groups.getLongPollServer(group_id=195861998)
server = info['server']
key = info['key']
ts = info['ts']

while True:

    vkapi.groups.setLongPollSettings(group_id=195861998, message_new=1)

    response = requests.get('{server}?act=a_check&key={key}&ts={ts}&wait=25'.format(server=server,
        key=key, ts=ts)).json()

    if 'updates' not in response:
        continue

    user_id = ''
    msg = ''
    for el in response['updates']:
        user_id = el['object']['user_id']
        msg = el['object']['body']

    try:
        vkapi.messages.send(user_id=user_id, random_id=rnd(1,2**63), peer_id=user_id, message=msg)
    except VkAPIError:
        continue

    ts = str(int(ts) + 1)