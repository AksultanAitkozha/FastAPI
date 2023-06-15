from pydantic import BaseSettings

from app.config import database

from .adapters.jwt_service import JwtService
from .repository.repository import AdsRepository
from .adapters.s3_service import S3Service
from .adapters.here_service import HereService


class AuthConfig(BaseSettings):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = "YOUR_SUPER_SECRET_STRING"
    JWT_EXP: int = 10_800
    HERE_API_KEY: str = "bmsTfHyGJo0dIvI5oMkhd6DIkAj5XMqU7vkx_w6cCA8"


config = AuthConfig()


class Service:
    def __init__(
        self,
        repository: AdsRepository,
        jwt_svc: JwtService,
        s3_service: S3Service,
    ):
        self.repository = repository
        self.jwt_svc = jwt_svc
        self.s3_service = s3_service
        self.here_service = HereService(config.HERE_API_KEY)


def get_service():
    repository = AdsRepository(database)
    jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)
    s3_service = S3Service()
    svc = Service(repository, jwt_svc, s3_service)
    return svc
