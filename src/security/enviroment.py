from pydantic_settings import BaseSettings, SettingsConfigDict


class Enviroment(BaseSettings):
    DB_DRIVE: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    JWT_SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file='.env')


# env_settings = Enviroment().model_dump()
