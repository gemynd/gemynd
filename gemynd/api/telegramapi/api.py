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

import telegram
import logging
import pg8000
from gemynd import Config
from gemynd import Database
from gemynd.core import Message
from gemynd.api.telegramapi import Users, Chats

logger = logging.getLogger(__name__)

class Telegram:


    def __init__(self, config):
        try:
            if (config['verbose'] == 'on'):
                logger.setLevel(logging.DEBUG)
            self.bot = telegram.Bot(token = config['api']['telegram']['token'])
            self.users = Users(config)
            self.chats = Chats(config)
            self.db = Database(config)
            self.db.connect()
            self.source = self.getSourceID()
        except Exception, ex:
            logger.error('Exception occured initializing the bot')
            logger.error('%s' % str(ex))
            raise ex


    def getInfo(self):
        self.bot.getMe()


    def getSourceID(self):
        retset = self.db.fetch(
             """select id
                    from core.sources
                    where source = 'telegram'
             """)
        if len(retset) == 0:
            raise Exception("Source ID for 'telegram' is not found")
        return retset[0][0]


    def getLastUpdate(self):
        retset = self.db.fetch(
             """select update_id
                    from telegram.updates
                    where id = (
                        select max(id)
                        from telegram.updates
                    )""")
        last_update_id = 0
        if len(retset) > 0:
            last_update_id = retset[0][0]
        logger.debug("Last update fetched from database is: %d" % last_update_id)
        return last_update_id


    def setLastUpdate(self, last_update_id):
        self.db.call("insert into telegram.updates (update_id) values (%d)" % last_update_id)
        logger.debug("New last update written to database is: %d" % last_update_id)


    def fetchDbBufferMessages(self, last_update_id):
        retset = self.db.fetch(
             """select  id,
                        chat_id,
                        message
                    from telegram.message_buffer
                    where update_id > %d
             """ % last_update_id)
        res = []
        if len(retset) > 0:
            for msg in retset:
                res.append(
                    Message(id        = msg[0],
                            chat_id   = msg[1],
                            text      = msg[2])
                    )
            retset = self.db.fetch("select max(update_id) from telegram.message_buffer")
            last_update_id = retset[0][0]
        return res, last_update_id


    def putDbBufferMessage(self, update_id, msg):
        self.db.call(
             """insert into telegram.message_buffer (update_id, id, chat_id, message)
                    values (%d, %d, %d, '%s')""" %
                    (update_id,
                     msg.id,
                     msg.chat_id,
                     msg.text.replace("'", "''"))
            )
        return


    def putDbMessage(self, msg, direction):
        self.db.call(
             """insert into core.messages (source_id,
                                           source_message_id,
                                           direction,
                                           chat_id,
                                           message)
                    values (%d, %d, '%s', %d, '%s')""" %
                    (self.source,
                     msg.id,
                     direction,
                     msg.chat_id,
                     msg.text.replace("'", "''"))
                )
        return


    def getNewMessages(self):

        last_update_id = self.getLastUpdate()
        dbmessages, last_update_id = self.fetchDbBufferMessages(last_update_id)
        new_update_id = last_update_id
        
        apimessages = []
        updates = self.bot.getUpdates(offset = last_update_id + 1)
        for item in updates:
            msg = item.message
            new_update_id = max(new_update_id, item.update_id)
            user_id = self.users.getUser(msg.from_user.id, msg.from_user.name)
            chat_id = self.chats.getChat(msg.chat_id, user_id)
            apimessages.append(
                Message(id = item.update_id,
                        chat_id = chat_id,
                        text = msg.text)
                )
            self.putDbBufferMessage(item.update_id, apimessages[-1])
            self.putDbMessage(apimessages[-1], 'I')

        result = list(set(dbmessages + apimessages))

        return result, new_update_id


    def commitNewMessages(self, new_update_id):
        self.setLastUpdate(new_update_id)
        self.db.call("delete from telegram.message_buffer where update_id <= %d" % new_update_id)


    def sendMessage(self, msg):
        telegram_chat_id = self.chats.getCoreChat(msg.chat_id)
        self.bot.sendMessage(chat_id = telegram_chat_id, text = msg.text)
        self.putDbMessage(msg, 'O')

    
    def close(self):
        self.db.close()