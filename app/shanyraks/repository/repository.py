from typing import Any, List

from datetime import datetime

import pytz

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

    def upload_urls(self, ad_id: str, user_id: str, image_urls: List[str]):
        """
        Adds the provided image URLs to the ad with the given id.
        """
        ad = self.get_ad_by_id(ad_id)

        if "image_urls" in ad:
            ad["media"].extend(image_urls)
        else:
            ad["media"] = image_urls

        return self.update_ad(ad_id, user_id, ad)

    def get_file_details(self, ad_id: str):
        return self.database["ads"].find_one({"_id": ObjectId(ad_id)})

    def delete_media(self, ad_id: str, user_id: str, media: List[str]) -> UpdateResult:
        return self.database["ads"].update_one(
            filter={"_id": ObjectId(ad_id), "user_id": ObjectId(user_id)},
            update={
                "$pull": {"media": {"$in": media}},
            },
        )

    def create_comment(self, ad_id: str, user_id: str, content: str):
        # timestamp of a tweet is based on Almaty timezone 
        almaty_tz = pytz.timezone("Asia/Almaty")
        now = datetime.now(almaty_tz)
        return self.database["ads"].update_one(
            {"_id": ObjectId(ad_id)},
            {"$push": {
                "comments": {
                    "_id": ObjectId(),
                    "author_id": ObjectId(user_id),
                    "content": content,
                    "created_at": now,  # This adds the current UTC time
                }
            }},
        )

    def get_comments(self, ad_id: str) -> List[dict]:
        ads = self.database["ads"].find({"_id": ObjectId(ad_id)}, {"comments": 1})
        result = []
        for ad in ads:
            for comment in ad["comments"]:
                comment["_id"] = str(comment["_id"])
                comment["author_id"] = str(comment["author_id"])
                comment["created_at"] = comment["created_at"].isoformat()
                result.append(comment)
        return result
