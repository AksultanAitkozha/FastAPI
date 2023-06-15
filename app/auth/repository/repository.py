from datetime import datetime
from typing import Optional, List

from bson.objectid import ObjectId
from pymongo.database import Database
from fastapi import Response

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user

    def update_user(self, user_id: str, input: dict) -> None:
        # payload dictionary to process data
        payload = {
            "phone": input.get("phone"),
            "name": input.get("name"),
            "city": input.get("city"),
        }
        # update the mongodb
        self.database["users"].update_one(
            {
                "_id": ObjectId(user_id),
            },
            {"$set": payload},
        )

    def add_to_favorites(self, user_id: str, ad_id: str) -> Optional[bool]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )

        if user:
            # Check if the ad is not already in the favorites
            if "favorites" in user and ad_id in user["favorites"]:
                # Return False if the ad is already in favorites
                return False
            else:
                # Check if the 'favorites' field exists, if not create it
                if "favorites" not in user:
                    self.database["users"].update_one(
                        {"_id": ObjectId(user_id)},
                        {"$set": {"favorites": []}},
                    )

                # Use $push operator to add the ad to favorites
                self.database["users"].update_one(
                    {"_id": ObjectId(user_id)},
                    {"$push": {"favorites": ad_id}},
                )
                return True
        else:
            # Raise an error if the user is not found
            return Response(status_code=404, detail="User not found")

    def get_favorites(self, user_id: str) -> Optional[List[dict]]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        if user:
            # If 'favorites' field doesn't exist, return an empty list
            if "favorites" not in user:
                return []

        # Otherwise, fetch the details of each ad in favorites and return the list
            favorites = []
            for ad_id in user["favorites"]:
                ad = self.database["ads"].find_one(
                    {
                        "_id": ObjectId(ad_id),
                    }
                )
                if ad:
                    favorites.append({"_id": ObjectId(ad_id), "address": ad["address"]})

            return favorites
        else:
            # Raise an HTTPException if the user is not found
            return Response(status_code=400)

    def remove_from_favorites(self, user_id: str, ad_id: str) -> Optional[bool]:
        result = self.database["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"favorites": ad_id}}
        )
        return result.modified_count > 0

    def upload_avatar(self, user_id: str, url: str) -> Optional[bool]:
        result = self.database["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"avatar_url": url}}
        )
        return result.modified_count > 0

    def delete_avatar(self, user_id: str) -> None:
        # Update the user's document to remove the avatar_url field
        self.database["users"].update_one({"_id": ObjectId(user_id)}, {"$unset": {"avatar_url": ""}})
