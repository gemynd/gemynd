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