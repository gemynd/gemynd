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

from functools import total_ordering

@total_ordering
class Message:

    def __init__(self, id, chat_id, text):
        self.id = id
        self.chat_id = chat_id
        self.text = text


    def __str__(self):
        result = {'id': self.id,
                  'chat_id': self.chat_id,
                  'text': self.text}
        return str(result)


    def __hash__(self):
        return hash(self.id)


    def __eq__(self, other):
        return (self.id == other.id)


    def __lt__(self, other):
        return (self.id < other.id)