#!/usr/bin/env python
#
# A library that provides a Gemynd AI bot interface
# Copyright (C) 2016
# Gemynd AI Team <devs@gemynd.ai>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import logging
import pg8000
from gemynd import Config
from gemynd import Database

logger = logging.getLogger(__name__)

class Chats:

    def __init__(self, config):
        try:
            if (config['verbose'] == 'on'):
                logger.setLevel(logging.DEBUG)
            self.db = Database(config)
            self.db.connect()
            self.telegramChats = dict()
            self.coreChats = dict()
        except Exception, ex:
            logger.error('Exception occured initializing chat list')
            logger.error('%s' % str(ex))


    def getTelegramChat(self, telegram_id):
        if not telegram_id in self.telegramChats:
            retset = self.db.fetch(
                 """select chat_id
                        from telegram.chats
                        where telegram_id = %d
                    """ % telegram_id)
            if len(retset) > 0:
                self.telegramChats[telegram_id] = retset[0][0]
        return self.telegramChats.get(telegram_id)


    def addTelegramChat(self, chat_id, telegram_id):
        self.db.call(
             """insert into telegram.chats (chat_id, telegram_id)
                    values (%d, %d)""" % (chat_id, telegram_id))
        self.telegramChats[telegram_id] = chat_id
        return


    def getCoreChat(self, chat_id):
        if not chat_id in self.coreChats:
            retset = self.db.fetch(
                 """select telegram_id
                        from telegram.chats
                        where chat_id = %d""" % chat_id)
            if len(retset) == 0:
                raise Exception("Cannot find telegram chat with chat_id = %d" % chat_id)
            self.coreChats[chat_id] = retset[0][0]
        return self.coreChats.get(chat_id)


    def addCoreChat(self, user_id):
        retset = self.db.fetch(
             """insert into core.chats (id, user_id)
                    values (DEFAULT, '%s')
                    returning id""" % user_id)
        return retset[0][0]


    def getChat(self, telegram_id, user_id):
        chat_id = self.getTelegramChat(telegram_id)
        if chat_id is None:
            chat_id = self.addCoreChat(user_id)
            self.addTelegramChat(chat_id, telegram_id)
        logger.debug("Telegram chat id '%d' with user '%d' has core id '%d'" %
                (telegram_id, user_id, chat_id))
        return chat_id


    def close(self):
        self.db.close()