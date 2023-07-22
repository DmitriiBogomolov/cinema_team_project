import pytest
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from tests.functional.fixtures.mongo import mongo_fixture

from tests.config import mongo_config


@pytest.fixture(scope='session')
def db():
    mongo_client = MongoClient(
        mongo_config.uri, server_api=ServerApi('1')
    )
    yield mongo_client['ugc_db']


@pytest.fixture(autouse=True)
def clean_mongo(db):
    db['bookmarks'].delete_many({})
    db['filmworks_likes'].delete_many({})
    db['reviews'].delete_many({})
    db['reviews_likes'].delete_many({})


@pytest.fixture()
def reviews_fix(clean_mongo, db):
    db['reviews'].insert_many(mongo_fixture['reviews'])


@pytest.fixture()
def bookmarks_fix(clean_mongo, db):
    db['bookmarks'].insert_many(mongo_fixture['bookmarks'])


@pytest.fixture()
def filmworks_likes_fix(clean_mongo, db):
    db['filmworks_likes'].insert_many(mongo_fixture['filmworks_likes'])


@pytest.fixture()
def reviews_likes_fix(clean_mongo, db):
    db['reviews_likes'].insert_many(mongo_fixture['reviews_likes'])
