from typing import Optional
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from .errors import CustomHTTPError, ExceptionCodes


class MongoManager:
    __instance: Optional[MongoClient] = None
    client: AsyncIOMotorClient = None
    DB = 'winners_coffee'
    mongo_customers_col = 'customers'

    def __init__(self, host, port, username, password):
        self.mongo_host = host
        self.mongo_port = int(port)
        self.mongo_username = username
        self.mongo_password = password

    async def connect(self):
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(
            self.mongo_host, self.mongo_port, username=self.mongo_username, password=self.mongo_password
        )

    async def disconnect(self):
        self.client.close()

    async def get_user_by_token(self, token):
        profile = await self.client[self.DB][self.mongo_customers_col].find_one({'token': token})
        if profile is None:
            raise CustomHTTPError(ExceptionCodes.TokenNotFound)
        if not profile['is_confirmed']:
            raise CustomHTTPError(ExceptionCodes.FirstLogin)
        return profile
