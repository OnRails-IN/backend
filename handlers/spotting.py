import json

from utils.spotting import *

def new_spotting_handler(event, context):
    if not event or not isinstance(event, dict):
        return { "status": 400 }
    if "body" not in event or not event['body'] or not isinstance(event['body'], str):
        return { "status": 400 }
    body = json.loads(event['body'])
    if not isinstance(body, dict) or len(body) < 1 or not { "username", "spotting_category" }.issubset(body):
        return { "status": 400 }
    last = most_recent_spotting()
    if last:
        lastId = int(last['_id'].replace("SPOT", ""))
        if lastId < 1000:
            nextId = str(lastId + 1).zfill(4)[-4]
        else:
            nextId = str(lastId + 1)
    else:
        nextId = "SPOT0001"
    createRes = create_spotting(nextId, body)
    if createRes is None:
        pass
    if createRes:
        return { "status": 201, "body": body }
    return { "status": 409 }