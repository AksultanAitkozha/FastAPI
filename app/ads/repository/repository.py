from datetime import datetime

from bson.objectid import ObjectId
from pymongo.database import Database


class AdsRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_new_ad(self, user_id: str, input: dict) -> str:
        payload = {
            "user_id": ObjectId(user_id),  # Assuming user_id is a valid ObjectId
            "type": input["type"],
            "price": input["price"],
            "address": input["address"],
            "area": input["area"],
            "rooms_count": input["rooms_count"],
            "description": input["description"],
            "created_at": datetime.utcnow(),
        }

        result = self.database["ads"].insert_one(payload)

        return str(result.inserted_id)  # Convert ObjectId to str
