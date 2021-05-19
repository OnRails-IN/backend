import json

from utils.user import login_user, signup_user, logout_user
from utils.redis import delete_key

"""
REQUEST STRUCTURE
{
    "resource": "/",
    "path": "/",
    "httpMethod": "GET",
    "requestContext": {
        "resourcePath": "/",
        "httpMethod": "GET",
        "path": "/Prod/",
        ...
    },
    "headers": {
        "accept": "text/html",
        "accept-encoding": "gzip, deflate, br",
        "Host": "xxx.us-east-2.amazonaws.com",
        "User-Agent": "Mozilla/5.0",
        ...
    },
    "multiValueHeaders": {
        "accept": [
            "text/html"
        ],
        "accept-encoding": [
            "gzip, deflate, br"
        ],
        ...
    },
    "queryStringParameters": {
        "postcode": 12345
    },
    "multiValueQueryStringParameters": null,
    "pathParameters": null,
    "stageVariables": null,
    "body": null,
    "isBase64Encoded": false
}
"""
def user_login_handler(event, context):
    if not event or not isinstance(event, dict):
        return { "status": 400 }
    if "body" not in event or not event['body'] or not isinstance(event['body'], str):
        return { "status": 400 }
    body = json.loads(event['body'])
    if not isinstance(body, dict) or len(body) < 1 or not { "username", "password" }.issubset(body):
        return { "status": 400 }
    loginRes = login_user(body['username'], body['password'])
    if loginRes is None:
        return { "status": 500 }
    if loginRes:
        return { "status": 200, "body": json.dumps(loginRes) }
    return { "status": 404 }

def user_logout_handler(event, context):
    if not event or not isinstance(event, dict):
        return { "status": 400 }
    if "headers" not in event or not event['headers']:
        return { "status": 400 }
    headers = event['headers']
    token = headers['Authorization'].replace("Bearer ", "")
    if len(token) < 1:
        return { "status": 400 }
    logoutRes = delete_key(token)
    if logoutRes is None:
        return { "status": 400 }
    if logoutRes:
        return { "status": 200 }
    return { "status": 409 }

def new_user_handler(event, context):
    if not event or not isinstance(event, dict):
        return { "status": 400 }
    if "body" not in event or not event['body'] or not isinstance(event['body'], str):
        return { "status": 400 }
    body = json.loads(event['body'])
    if not isinstance(body, dict) or len(body) < 1 or not { "username", "password", "email" }.issubset(body):
        return { "status": 400 }
    signUpRes = signup_user(body)
    if signUpRes is None:
        return { "status": 500 }
    if signUpRes:
        return { "status": 201, "body": json.dumps(body) }
    return { "status": 409 }