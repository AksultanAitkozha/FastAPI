from typing import Any

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


class AdsRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_new_ad(self, user_id: str, load: dict[str, Any]):
        load["user_id"] = ObjectId(user_id)

        result = self.database["ads"].insert_one(load)

        return result.inserted_id  # Convert ObjectId to str

    def get_ad_by_id(self, ad_id: str):
        return self.database["ads"].find_one({"_id": ObjectId(ad_id)})

    def update_ad(self, ad_id: str, user_id: str, load: dict[str, Any]) -> UpdateResult:
        return self.database["ads"].update_one(
            filter={"_id": ObjectId(ad_id), "user_id": ObjectId(user_id)},
            update={
                "$set": load,
            },
        )

    def delete_ad(self, ad_id: str, user_id: str) -> DeleteResult:
        return self.database["ads"].delete_one(
            {"_id": ObjectId(ad_id), "user_id": ObjectId(user_id)}
        )
