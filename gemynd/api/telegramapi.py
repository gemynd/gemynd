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
from gemynd.core import Message

logger = logging.getLogger(__name__)

class Telegram:


    def __init__(self, token):
        try:
            self.bot = telegram.Bot(token=token)
        except Exception, ex:
            logger.error('Exception occured initializing the bot')
            logger.error('%s' % str(ex))


    def getInfo(self):
        self.bot.getMe()


    def getMessages(self):
        result = []
        updates = self.bot.getUpdates()
        for item in updates:
            msg = item.message
            result.append(
                Message(id = msg.message_id,
                        user_id = msg.from_user.id,
                        user_name = msg.from_user.name,
                        chat_id = msg.chat_id,
                        text = msg.text)
                )
        return result


    def sendMessage(self, chat_id, text):
        self.bot.sendMessage(chat_id = chat_id, text = text)


    def answerAll(self, text):
        updates = self.getMessages()
        for chat_id in set([u.chat_id for u in updates]):
            self.sendMessage(chat_id, text)
