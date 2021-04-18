"""
Journey Utils
=============

All utility functions to manage journey documents in Elasticsearch
The index user is "user-journeys-<current year>"

Functions
    - create_journey
    - list_journeys
    - most_recent_journey
    - get_journey
    - update_journey
    - add_halt_to_journey
    - deactivate_journey
    - delete_journey
"""
import time
from elasticsearch import NotFoundError

from elastic import create_or_update_document, list_documents, get_document, update_journey, delete_document

INDEX = "user-journeys-" + time.strftime("%Y")

def create_journey(ID, body):
    """
    Function to create a new journey document in Elasticsearch
    
    Params:
        ID::str
            id for the journey document
        body::dict
            Object to be stored as journey document
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
        global INDEX
        create_or_update_document(INDEX, ID, body)
        return True

    except Exception as e:
        print("Exception @ create_spotting\n{}".format(e))
        return False

def list_journeys(includeInactive = False):
    """
    Function to list all the journey documents in Elasticsearch

    Params:
        includeInactive::bool
            If inactive records must be included in the result or not
    Returns:
        total_docs::int
            The total number of records
        docs::[dict]
            The list of documents
    """
    try:
        query = {} if includeInactive else { "query": { "term": { "is_active": True } } }
        global ES, INDEX
        search = list_documents(INDEX, query)
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
            If most recent journey of a particular user
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
        global INDEX
        search = list_documents(INDEX, query)
        return { '_id': search['hits'][0]['_id'], **search['hits'][0]['_source'] }

    except NotFoundError:
        print("No documents found @ most_recent_journey")
        return False

    except Exception as e:
        print("Exception @ most_recent_journey\n{}".format(e))
        return False

def get_journey(ID):
    """
    Function to get one document from Elasticsearch

    Params:
        ID::str
            id of the journey document
    Returns:
        doc::dict
            The document retrieved from ES
    """
    if not ID:
        return False

    try:
        global INDEX
        ref = get_document(INDEX, ID)
        return { '_id': ref['_id'], **ref['_source'] }

    except NotFoundError:
        print("No documents found at get_journey")
        return False

    except Exception as e:
        print("Exception @ get_journey\n{}".format(e))
        return False

def update_journey(ID, changes):
    """
    Function to update a journey document in Elasticsearch

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
        global INDEX
        changes['updated_timestamp'] = int(time.time())
        body = get_document(INDEX, ID)['_source']
        create_or_update_document(INDEX, ID, { **body, **changes })
        return True

    except NotFoundError:
        print("No documents found at update_journey")
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
    if not ID or "station" not in haltObj:
        return False

    try:
        global INDEX
        body = get_document(INDEX, ID)['_source']
        if 'halts' in body and haltObj not in body['halts']:
            body['halts'].append(haltObj)
        else:
            body['halts'] = [haltObj]
        create_or_update_document(INDEX, ID, body)
        return True

    except NotFoundError:
        print("No documents found at add_halt_to_journey")
        return False

    except Exception as e:
        print("Exception @ add_halt_to_journey\n{}".format(e))
        return False

def deactivate_journey(ID):
    """
    Function to deactivate a journey document in Elasticsearch

    Params:
        ID::str
            id of the document to deactivate
    Returns:
        bool
            If the changes have been applied or not
    """
    if not ID:
        return False

    try:
        global INDEX
        body = get_document(INDEX, ID)['_source']
        body['is_active'] = False
        create_or_update_document(INDEX, ID, body)
        return True

    except NotFoundError:
        print("No documents found at deactivate_journey")
        return False

    except Exception as e:
        print("Exception @ deactivate_journey\n{}".format(e))
        return False

def delete_journey(ID):
    """
    Function to delete a journey document on Elasticsearch

    Params:
        ID::str
            ID of the document to delete
    Returns:
        bool
            If the document is deleted or not
    """
    try:
        global INDEX
        delete_document(INDEX, ID)
        return True

    except NotFoundError:
        print("No documents found at delete_journey")
        return False

    except Exception as e:
        print("Exception @ delete_journey\n{}".format(e))
        return False