from sqlalchemy import URL, create_engine

from ..security.enviroment import env_settings

# pra testes
engine = create_engine('sqlite:///:memory:')

#    DB_URL = URL.create(
#        drivername=env_settings['DB_DRIVE'],
#        username=env_settings['DB_USERNAME'],
#        password=env_settings['DB_PASSWORD'],
#       host=env_settings['DB_HOST'],
#        port=env_settings['DB_PORT'],
#        database=env_settings['DB_NAME'],
#)

# print(DB_URL)
