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

import json
import logging

logger = logging.getLogger(__name__)

class Config:

    def __init__(self, filename):
        self.map = {}
        try:
            f = open(filename, 'rb')
            self.map = json.load(f)
        except Exception, ex:
            logger.error('Cannot load configuration')
            logger.error(str(ex))


    def __getitem__(self, key):
        return self.map[key]
