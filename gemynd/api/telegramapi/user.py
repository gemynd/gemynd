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

class Users:

    def __init__(self, config):
        try:
            if (config['verbose'] == 'on'):
                logger.setLevel(logging.DEBUG)
            self.db = Database(config)
            self.db.connect()
            self.telegramUsers = dict()
        except Exception, ex:
            logger.error('Exception occured initializing user list')
            logger.error('%s' % str(ex))


    def getTelegramUser(self, telegram_id):
        if not telegram_id in self.telegramUsers:
            retset = self.db.fetch(
                 """select user_id
                        from telegram.users
                        where telegram_id = %d
                    """ % telegram_id)
            if len(retset) > 0:
                self.telegramUsers[telegram_id] = retset[0][0]
        return self.telegramUsers.get(telegram_id)


    def getCoreUser(self, user_name):
        retset = self.db.fetch(
             """select id
                    from core.users
                    where name = '%s'
                """ % user_name)
        return retset


    def addTelegramUser(self, user_id, telegram_id):
        self.db.call(
             """insert into telegram.users (user_id, telegram_id)
                    values (%d, %d)""" % (user_id, telegram_id))
        return


    def addCoreUser(self, user_name):
        self.db.call(
             """insert into core.users (name)
                    values ('%s')""" % user_name)
        return self.getCoreUser(user_name)


    def getUser(self, telegram_id, user_name):
        user_id = self.getTelegramUser(telegram_id)
        if user_id is None:
            retset = self.getCoreUser(user_name)
            if len(retset) == 0:
                retset = self.addCoreUser(user_name)
            user_id = retset[0][0]
            self.addTelegramUser(user_id, telegram_id)
            self.getTelegramUser(telegram_id)
        logger.debug("Telegram user id '%d' name '%s' has core id '%d'" %
                (telegram_id, user_name, user_id))
        return user_id


    def close(self):
        self.db.close()