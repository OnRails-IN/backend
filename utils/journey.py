import time
from elasticsearch import Elasticsearch, NotFoundError

from constants import ES_URI
ES = Elasticsearch([ ES_URI ])
INDEX = "user-journeys-" + time.strftime("%Y")

def create_journey(ID, body):
    """
    Function to create a new journey document in Elasticsearch
    
    Params:
        ID::str
            id of the document to be created
        body::dict
            Body object which is to become the document
    Returns:
        bool
            If the document is created or not
    """
    # Required fields check
    if not ID or not body or not {'username', 'train_number', 'from'}.issubset(body):
        return False

    try:
        if 'timestamp' not in body:
            body['timestamp'] = int(time.time())
        if 'is_active' not in body:
            body['is_active'] = True
        global ES, INDEX
        ES.index(index = INDEX, id = ID, body = body)
        return True

    except Exception as e:
        print("Exception @ create_journey\n{}".format(e))
        return False

def list_journeys(includeInactive = False):
    """
    Function to list all the journey documents in Elasticsearch

    Params:
        includeInactive::bool
            If in active records must be included in the result or not
    Returns:
        total_docs::int
            The total number of records retrieved
        docs::[dict]
            The documents retrieved from the ES index
    """
    try:
        query = {} if includeInactive else { "query": { "term": { "is_active": True } } }
        global ES, INDEX
        search = ES.search(query, index = INDEX, _source = True)['hits']
        docs = [{ '_id': hit['_id'], **hit['_source'] } for hit in search['hits']]
        return { 'total_docs': len(docs), 'docs': docs }

    except NotFoundError:
        print("No documents found at list_journeys")
        return None

    except Exception as e:
        print("Exception @ list_journeys\n{}".format(e))
        return None

def most_recent_journey(username = None):
    """
    Function to retrieve most recent journey document from Elasticsearch

    Params:
        username::str
            If most recent journey of a particular user is required
    Returns:
        doc::dict
            The most recent doucment in the ES index
    """
    try:
        query = {
            "sort": [
                { "timestamp": "desc" }
            ],
            "size": 1
        }
        if username:
            query['query'] = { "term": { "username": username } }
        global ES, INDEX
        search = ES.search(query, index = INDEX, _source = True)['hits']
        return { "_id": search['hits'][0]['_id'], **search['hits'][0]['_source'] }

    except NotFoundError:
        print("No documents found @ most_recent_journey")
        return False

    except Exception as e:
        print("Exception @ most_recent_journey\n{}".format(e))
        return False

def get_journey(ID):
    """
    Function to retrieve one document from Elasticsearch

    Params:
        ID::str
            id of the document to retrieve
    Returns:
        doc::dict
            The document retireved from the ES index
    """
    if not ID:
        return False

    try:
        global ES, INDEX
        ref = ES.get(index = INDEX, id = ID)
        return { '_id': ref['_id'], **ref['_source'] }

    except NotFoundError:
        return False

    except Exception as e:
        print("Exception @ get_journey\n{}".format(e))
        return False

def update_journey(ID, changes):
    """
    Function to update a document in the Elasticsearch index

    Params:
        ID::str
            id of the document to update
        changes::dict
            Changes to be made to the document
    Returns:
        bool
            If the changes have been applied or not
    """
    if not ID:
        return False

    try:
        if '_id' in changes:
            del changes['_id']
        changes['updated_timestamp'] = int(time.time())
        global ES, INDEX
        body = ES.get(index = INDEX, id = ID)['_source']
        body = { **body, **changes }
        ES.index(index = INDEX, id = ID, body = body)
        return True

    except NotFoundError:
        return False

    except Exception as e:
        print("Exception @ update_journey\n{}".format(e))
        return False

def add_halt_to_journey(ID, haltObj):
    """
    Function to add one halt to the journey document in Elasticsearch

    Params:
        ID::str
            id of the document to update
        haltObj::dict
            The data to be added to the document
    Returns:
        bool
            If the changes have been applied or not
    """
    if not ID:
        return False
    if "station" not in haltObj:
        return False

    try:
        global ES, INDEX
        body = ES.get(index = INDEX, id = ID)['_source']
        if 'halts' in body and haltObj not in body['halts']:
            body['halts'].append(haltObj)
        else:
            body['halts'] = [haltObj]
        ES.index(index = INDEX, id = ID, body = body)
        return True

    except NotFoundError:
        return False

    except Exception as e:
        print("Exception @ add_halt_to_journey\n{}".format(e))
        return False

def deactivate_journey(ID):
    """
    Function to deactivate a journey document in Elasticsearch

    Params:
        ID::str
            id of the document to update
    Returns:
        bool
            If the changes have been applied or not
    """
    if not ID:
        return False

    try:
        global ES, INDEX
        body = ES.get(index = INDEX, id = ID)['_source']
        body['is_active'] = False
        ES.index(index = INDEX, id = ID, body = body)
        return True

    except NotFoundError:
        return False

    except Exception as e:
        print("Exception @ deactivate_journey\n{}".format(e))
        return False