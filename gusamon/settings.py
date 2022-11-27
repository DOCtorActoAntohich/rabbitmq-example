from pydantic import BaseSettings, Field


class _RabbitMqSettings(BaseSettings):
    queue: str = Field("monqueue")
    host: str = Field(..., env="RABBITMQ_HOST")
    username: str = Field(..., env="RABBITMQ_USER")
    password: str = Field(..., env="RABBITMQ_PASS")

    @property
    def url(self):
        return f"amqp://{self.username}:{self.password}@{self.host}"


class Settings:
    rabbitmq = _RabbitMqSettings()
