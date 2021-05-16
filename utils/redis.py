"""
Redis Utils
===========

All utility functions for interactions with redis server

Functions:
    - set_data
    - get_data
    - delete_key
"""
import json
import time
from redis import Redis
from base64 import urlsafe_b64encode

from constants import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

rds = Redis(host = REDIS_HOST, port = REDIS_PORT, password = REDIS_PASSWORD)

def set_data(data, key = None):
    """
    Function to create a Redis key

    Params:
        data::dict|list
            The data to be cached
        key::str
            The key to store the data in
    Returns:
        cacheKey::str
            The cacheKey in which the data has been stored

    """
    if not data:
        return False
    if not isinstance(data, dict) and not isinstance(data, list):
        return False

    try:
        if key is not None and key:
            # Key to store passed as param
            cacheKey = key
        else:
            if isinstance(data, dict) and "username" in data:
                # Data obj contains "username" key
                cacheKey = "UserCache_" + urlsafe_b64encode(data['username'].encode('ascii')).decode()
            else:
                # Data is not dict or "username" is not present
                cacheKey = "MiscCache_" + str(int(time.time()))
        rds.set(cacheKey, json.dumps(data))
        return cacheKey

    except Exception as e:
        print("Exception @ set_data\n{}".format(e))
        return None

def get_data(key):
    """
    Retrieve data from Redis

    Params:
        key::str
            The cache key to fetch
    Returns:
        data::dict
            The data stored in the key
    """
    if not key:
        return False

    try:
        return json.loads(rds.get(key).decode())

    except Exception as e:
        print("Exception @ get_data\n{}".format(e))
        return None

def delete_key(key):
    """
    Function to delete a key in Redis

    Params:
        key::str
            The cache key to delete
    Returns:
        bool
            If the cache has been deleted or not
    """
    if not key:
        return False

    try:
        rds.delete(key)
        return True

    except Exception as e:
        print("Exception @ delete_key\n{}".format(e))
        return None