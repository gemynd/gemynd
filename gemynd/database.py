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

import pg8000
import logging
from gemynd import Config
import re

logger = logging.getLogger(__name__)

class Database:

    def __init__(self, config):
        self.connected = False
        self.db = config['db']
        if (config['verbose'] == 'on'):
            logger.setLevel(logging.DEBUG)


    def connect(self):
        try:
            logger.debug("Connecting to the database '%s' user '%s'" % (self.db['database'], self.db['username']))
            self.connection = pg8000.connect(
                    host = self.db['host'],
                    port = int(self.db['port']),
                    database = self.db['database'],
                    user = self.db['username'],
                    password = self.db['password'])
            self.connected = True
        except Exception, ex:
            logger.error('Cannot connect to the database')
            logger.error('%s' % str(ex))


    def execute(self, query, isdatareturned):
        res = None
        if not self.connected:
            logger.error('You should connect to the database prior to executing the query')
        else:
            try:
                logger.debug('Executing query "%s"' % re.sub('\s+', ' ', query.strip()))
                cursor = self.connection.cursor()
                cursor.execute(query)
                if isdatareturned:
                    res = cursor.fetchall()
                cursor.close()
                self.connection.commit()
            except Exception, ex:
                logger.error('Error happened while executing the query "%s"' % query)
                logger.error('%s' % str(ex))
        return res


    def fetch(self, query):
        return self.execute(query, True)


    def call(self, query):
        return self.execute(query, False)


    def close(self):
        logger.debug("Closing database connection to '%s' user '%s'" % (self.db['database'], self.db['username']))
        self.connection.close()
        self.connected = False