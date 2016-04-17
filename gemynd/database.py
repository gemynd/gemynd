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

logger = logging.getLogger(__name__)

class Database:

    def __init__(self, config):
        self.connected = False
        self.db = config['db']


    def connect(self):
        try:
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


    def close(self):
        self.connection.close()