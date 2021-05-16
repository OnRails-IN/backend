"""
Spotting Utils
==============

All utility functions to manage spotting documents in Elasticsearch
The index used is "user-spottings-<current year>"

Functions
    - create_spotting
    - list_spottings
    - get_spotting
    - update_spotting
    - deactivate_spotting
    - delete_spotting
"""
import time
from elasticsearch import NotFoundError

from .elastic import create_or_update_document, list_documents, get_document, delete_document

INDEX = "user-spottings-" + time.strftime("%Y")

def create_spotting(ID, body):
    """
    Function to create a new spotting document in Elasticsearch

    Params:
        ID::str
            id for the spotting document
        body::dict
            Object to be stored as spotting document
    Returns:
        bool
            If the document is created or not
    """
    # Required fields check
    if not ID or not {"username", "spotting_category"}.issubset(body):
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
        return None

def list_spottings(includeInactive = False):
    """
    Function to list all spotting documents from Elasticsearch

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
        global INDEX
        search = list_documents(INDEX, query)
        docs = [{ "_id": hit['_id'], **hit['_source'] } for hit in search['hits']]
        return { "total_docs": len(docs), "docs": docs }

    except NotFoundError:
        print("No documents found at list_journeys")
        return False

    except Exception as e:
        print("Exception @ list_spottings\n{}".format(e))
        return None

def get_spotting(ID):
    """
    Function to get one spotting document from Elasticsearch

    Params:
        ID::str
            id of the spotting document
    Returns:
        doc::dict
            The document retrieved from ES
    """
    if not ID:
        return False

    try:
        global INDEX
        ref = get_document(INDEX, ID)
        return { "_id": ref['_id'], **ref['_source'] }

    except NotFoundError:
        print("No documents found at get_spotting")
        return False

    except Exception as e:
        print("Exception @ get_spotting\n{}".format(e))
        return None

def update_spotting(ID, changes):
    """
    Function to update a spotting document in Elasticsearch

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
        print("No documents found at update_spotting")
        return False

    except Exception as e:
        print("Exception @ update_spotting\n{}".format(e))
        return None

def deactivate_spotting(ID):
    """
    Function to deactivate a spotting document in Elasticsearch

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
        print("No documents found at deactivate_spotting")
        return False

    except Exception as e:
        print("Exception @ deactivate_spotting\n{}".format(e))
        return None

def delete_spotting(ID):
    """
    Function to delete a spotting document on Elasticsearch

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
        print("No documents found at delete_spotting")
        return False

    except Exception as e:
        print("Exception @ delete_spotting\n{}".format(e))
        return None