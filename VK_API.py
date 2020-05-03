#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def create_session(group_id, token):
    api = vk_api.VkApi(token=token)
    longpoll = VkBotLongPoll(api, group_id)
    session = api.get_api()
    print('session created')
    return {'session': session, 'longpoll': longpoll}


def get_user(user_id, session):
    print('ug')
    return session.users.get(user_ids=user_id, fields='online')


def get_conversation(peer_id, session):
    return session.messages.getConversationsById(peer_id=peer_id)['items']


def get_conversation_members(peer_id, session):
    return session.messages.getConversationMembers(peer_id=peer_id)['profiles']


def get_conversations(session):
    return session.messages.getConversations()['items']


def get_event_type(event):
    print('etg')
    if event.type == VkBotEventType.MESSAGE_NEW:
        return 'MESSAGE_NEW'


def write_msg(session, session_event, text, sticker_id=None, picture=None):
    bot_msg = None
    if text and picture is None:
        bot_msg = session.messages.send(
            peer_id=session_event.obj['peer_id'],
            random_id=session_event.obj['random_id'],
            message=text
        )
    if sticker_id is not None:
        bot_msg = session.messages.send(
            peer_id=session_event.obj['peer_id'],
            random_id=session_event.obj['random_id'],
            sticker_id=sticker_id
        )
    if picture is not None:
        photo_file = session.photos.getMessagesUploadServer(
            peer_id=session_event.obj['peer_id'])
        r_data = {'photo': open('images/pitivo.jpg', 'rb')}
        photo_data = requests.post(photo_file['upload_url'], files=r_data).json()
        photo = session.photos.saveMessagesPhoto(server=photo_data['server'],
                                                         photo=photo_data['photo'],
                                                         hash=photo_data['hash'])[0]
        bot_msg = session.messages.send(
            peer_id=session_event.obj['peer_id'],
            random_id=session_event.obj['random_id'],
            message=text,
            attachment='photo{0}_{1}'.format(photo['owner_id'], photo['id'])
        )
    return bot_msg


def save_last_msg(session_event, text, dictionary):
    peer_id = session_event.obj['peer_id']
    dictionary[peer_id] = text

