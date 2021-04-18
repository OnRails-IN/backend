from elasticsearch import Elasticsearch, NotFoundError

from constants import ES_URI
ES = Elasticsearch([ ES_URI ])

def create_or_update_document(index, ID, body):
    """
    Function to create or update a document in Elasticsearch

    Params:
        index::str
            ES index of the document
        ID::str
            ID of the ES document
        body::dict
            Object to be stored as document body
    Returns:
        True / Exception
    """
    try:
        global ES
        ES.index(index = index, id = ID, body = body)
        return True

    except Exception as e:
        return e

def list_documents(index, query = {}):
    """
    Function to list all documents from Elasticsearch

    Params:
        index::str
            ES index to search for documents
        query::dict
            Query object to search
    Returns:
        docs::[dict]
            Documents retrieved from ES index
    """
    try:
        global ES
        return ES.search(query, index = index, _source = True)['hits']

    except Exception as e:
        return e

def get_document(index, ID):
    """
    Function to get one document from Elasticsearch

    Params:
        index::str
            ES index to get the document
        ID::str
            ID of the document
    Returns:
        doc::dict
            Document retrieved from ES index
    """
    try:
        global ES
        return ES.get(index = index, id = ID)

    except Exception as e:
        return e

def delete_document(index, ID):
    """
    Function to delete one document on Elasticsearch

    Params:
        index::str
            ES index of document to delete
        ID::str
            ID of the document to delete
    Returns:
        True / Exception
    """
    try:
        global ES
        ES.delete(index = index, id = ID)
        return True

    except Exception as e:
        return e