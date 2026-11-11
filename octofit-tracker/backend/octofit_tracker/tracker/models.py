from functools import lru_cache

from django.conf import settings
from pymongo import MongoClient


COLLECTION_NAMES = ("users", "teams", "activities", "workouts")


@lru_cache(maxsize=1)
def get_mongo_client():
    return MongoClient(settings.MONGODB_URI)


def get_database():
    return get_mongo_client()[settings.MONGODB_DATABASE]


def get_collection(name):
    if name not in COLLECTION_NAMES:
        raise ValueError(f"Unknown OctoFit collection: {name}")
    return get_database()[name]
