"""
User Utils
==========

All utility functions to manage new and existing users

Functions
    - validate_cache
    - signup_user
    - login_user
    - logout_user
    - existing_users
    - cache_existing_users
"""
import time
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet

from .redis import set_data, get_data, delete_key
from .dynamo import create_or_update_record, list_records, get_record, delete_record

from constants import SECRET_KEY, INDEX_KEYS
crypt = Fernet(SECRET_KEY)

def validate_cache(cacheKey, username = None):
    """
    Function to check if a cache key is valid
    If username is passed, checks if cache is for that user

    Params:
        cacheKey::str
            The cache key to validate
        username::str
    Returns:
        bool
            If the cache key is valid or not
    """
    if not cacheKey:
        return False

    try:
        cacheObj = get_data(cacheKey)
        if cacheObj['expiry_timestamp'] < int(time.time()):
            delete_key(cacheKey)
            return False
        if username and cacheObj['username'] != username:
            return False
        return True

    except Exception as e:
        print("Exception @ validate_cache\n{}".format(e))
        return False

def signup_user(body):
    """
    Function to sign up a new user

    Params:
        body::dict
            The object with the user details
    Returns:
        bool
            If the new user was created or not
    """
    if not body or not {'username', 'password'}.issubset(body):
        return False

    try:
        existingUsers = existing_users()
        if body['username'] in existingUsers:
            # Username already taken
            return False
        
        # TODO: Validate username
        
        body = {
            **body,
            'index': INDEX_KEYS[body['username'][0].lower()], # Create index
            'password': crypt.encrypt(body['password'].encode()).decode(), # Encrypt password
            'created_timestamp': int(time.time()) # Creation timestamp
        }
        if not create_or_update_record("users", body):
            return False
        cache_existing_users()
        return True

    except Exception as e:
        print("Exception @ signup_user\n{}".format(e))
        return False

def login_user(username, password):
    """
    Function to log in an existing user

    Params:
        username::str
        password::str
    Returns:
        key::str
            The cache key created on login
        expiry_timestamp::int
            The unix timestamp of cache expiry
    """
    if not username or not password:
        return False

    try:
        # Validate user
        record = get_record("users", { "username": username, "index": INDEX_KEYS[username[0].lower()] })
        
        if not record:
            return False
        if crypt.decrypt(record['password'].encode()).decode() == password:
            # User has been verified, Create login cache
            cacheObj = {
                "username": username,
                "login_timestamp": int(time.time()), # Cache timestamp
                "expiry_timestamp": int(time.time()) + 7200 # Cache expiry in 2hrs
            }
            # Return cache key & expiry
            return { "key": set_data(cacheObj), "expiry_timestamp": cacheObj['expiry_timestamp'] }

        else:
            return False

    except Exception as e:
        print("Exception @ login_user\n{}".format(e))
        return False

def logout_user(username):
    """
    Function to log out an existing user

    Params:
        username::str
    Returns:
        bool
            If the user has been logged out or not
    """
    if not username:
        return False

    try:
        cacheKey = "UserCache_" + urlsafe_b64encode(username.encode('ascii')).decode()
        return delete_key(cacheKey)

    except Exception as e:
        print("Exception @ logout_user\n{}".format(e))
        return False

def existing_users():
    """
    Function to get list of existing users

    Returns:
        users::[str]
            The list of existing users
    """
    try:
        cacheList = get_data("ExistingUserListCache")
        if cacheList:
            return cacheList['users']
        else:
            records = list_records("users")
            users = list(map(lambda r: r['username'] , records))
            return users

    except Exception as e:
        print("Exception @ existing_users\n{}".format(e))
        return False

def cache_existing_users():
    """
    Function to create a cache of list of existing users

    Returns:
        bool
            If the cache key was created or not
    """
    try:
        records = list_records("users")
        users = list(map(lambda r: r['username'] , records))
        set_data({ "users": users, "timestamp": int(time.time()) }, "ExistingUserListCache")
        return True

    except Exception as e:
        print("Exception @ cache_existing_users\n{}".format(e))
        return False