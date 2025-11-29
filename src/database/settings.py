from sqlalchemy import create_engine

from ..models.base import Base

# from ..security.enviroment import env_settings

engine = create_engine('sqlite:///database.db', echo=True)

Base.metadata.create_all(engine)

#    DB_URL = URL.create(
#        drivername=env_settings['DB_DRIVE'],
#        username=env_settings['DB_USERNAME'],
#        password=env_settings['DB_PASSWORD'],
#       host=env_settings['DB_HOST'],
#        port=env_settings['DB_PORT'],
#        database=env_settings['DB_NAME'],
# )

# print(DB_URL)
