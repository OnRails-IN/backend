"""
Dynamo Utils
============

All utility functions for interactions with DynamoDB

Functions
    - ensure_json
    - create_user_table
    - create_or_update_record
    - list_tables
    - list_records
    - get_record
    - delete_table
    - delete_record
    - check_active
"""
import boto3
from decimal import Decimal

from constants import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, DYNAMO_URL

ddb = boto3.resource(
    'dynamodb',
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_KEY,
    endpoint_url = DYNAMO_URL,
    region_name = AWS_REGION
)
client = boto3.client(
    'dynamodb',
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_KEY,
    endpoint_url = DYNAMO_URL,
    region_name = AWS_REGION
)

def ensure_json(obj):
    """
    Function to ensure that a python object is JSON serializable

    Params:
        obj::dict|[dict]
            Object to be JSON serializable
    Returns:
        obj::dict|[dict]
            Returns the JSON serializable object
    """
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = ensure_json(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = ensure_json(obj[k])
        return obj
    elif isinstance(obj, Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj

def create_user_table():
    """
    Function to create the "users" table in DynamoDB

    Returns:
        bool
            If the table was created or not
    """
    try:
        table = ddb.create_table(
            TableName = "users",
            KeySchema = [
                {
                    "AttributeName": "username",
                    "KeyType": "HASH" # Partition key
                },
                {
                    "AttributeName": "index",
                    "KeyType": "RANGE" # Sort key
                }
            ],
            AttributeDefinitions = [
                {
                    "AttributeName": "username",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "index",
                    "AttributeType": "S"
                }
            ],
            ProvisionedThroughput = {
                "ReadCapacityUnits": 10,
                "WriteCapacityUnits": 10
            }
        )
        return True

    except client.exceptions.ResourceNotFoundException:
        print("Table does not exist")
        return False

    except Exception as e:
        print("Exception @ create_user_table\n{}".format(e))
        return False

def create_train_table():
    """
    Function to create the "trains" table in DynamoDB

    Returns:
        bool
            If the table was created or not
    """
    try:
        table = ddb.create_table(
            TableName = "trains",
            KeySchema = [
                {
                    "AttributeName": "train_name",
                    "KeyType": "HASH" # Partition key
                },
                {
                    "AttributeName": "train_type",
                    "KeyType": "RANGE" # Sort key
                }
            ],
            AttributeDefinitions = [
                {
                    "AttributeName": "train_name",
                    "AttributeType": "N"
                },
                {
                    "AttributeName": "train_type",
                    "AttributeType": "S"
                }
            ],
            ProvisionedThroughput = {
                "ReadCapacityUnits": 10,
                "WriteCapacityUnits": 10
            }
        )
        return True

    except client.exceptions.ResourceNotFoundException:
        print("Table does not exist")
        return False

    except Exception as e:
        print("Exception @ create_user_table\n{}".format(e))
        return False

def create_or_update_record(tableName, record):
    """
    Function to create or update a record in DynamoDB

    Params:
        tableName::str
            The table name to get the record
        record::dict
            The object to store

    Returns:
        bool
            If the record was inserted or not
    """
    if not tableName or not record:
        return False
    if not {'username', 'index'}.issubset(record):
        return False

    try:
        res = ddb.Table(tableName).get_item(
            Key = {
                "username": record['username'],
                "index": record['index']
            }
        )
        record =  { **res['Item'], **record } if 'Item' in res else record
        ddb.Table(tableName).put_item(
            Item = record
        )
        return True

    except client.exceptions.ResourceNotFoundException:
        print("Table does not exist")
        return False

    except Exception as e:
        print("Exception @ create_or_update_record\n{}".format(e))
        return False

def list_tables():
    """
    Function to list all tables in DynamoDB

    Returns:
        tables::[str]
            The list of tables
    """
    try:
        return client.list_tables()['TableNames']

    except client.exceptions.ResourceNotFoundException:
        print("Tables do not exist")
        return None

    except Exception as e:
        print("Exception @ list_tables\n{}".format(e))
        return None

def list_records(tableName):
    """
    Function to list all records from a DynamoDB table

    Params:
        tableName::str
            The table name to get the records
    Returns:
        records::[dict]
            The list of records stored in the table
    """
    if not tableName:
        return None

    try:
        table = ddb.Table(tableName)
        res = table.scan()
        docs = ensure_json(res['Items'])
        while 'LastEvaluatedKey' in res:
            res = table.scan(ExclusiveStartKey = res['LastEvaluatedKey'])
            docs.extend(ensure_json(res['Items']))
        return docs

    except client.exceptions.ResourceNotFoundException:
        print("Table does not exist")
        return None

    except Exception as e:
        print("Exception @ list_records\n{}".format(e))
        return None

def get_record(tableName, query):
    """
    Function to retrieve one record from DynamoDB table

    Params:
        tableName::str
            The table name to get the record
        query::dict
            The query to fetch the record
    Returns:
        doc::dict
            The record retrieved from the table
    """
    if not tableName or not query or not isinstance(query, dict):
        return None

    try:
        res = ddb.Table(tableName).get_item(
            Key = query
        )
        doc = ensure_json(res['Item']) if 'Item' in res else None
        return doc

    except client.exceptions.ResourceNotFoundException:
        print("Table does not exist")
        return None

    except Exception as e:
        print("Exception @ get_record\n{}".format(e))
        return None

def delete_table(tableName):
    """
    Function to delete a DynamoDB table

    Params:
        tableName::str
            The table name to delete
    Returns:
        bool
            If the table was deleted or not
    """
    if not tableName:
        return False

    try:
        ddb.Table(tableName).delete()
        return True

    except client.exceptions.ResourceNotFoundException:
        print("Table does not exist")
        return False

    except Exception as e:
        print("Exception @ delete_table\n{}".format(e))
        return False

def delete_record(tableName, query):
    """
    Function to delete a DynamoDB table

    Params:
        tableName::str
            The table name to get the record
        query::dict
            The query to fetch the record
    Returns:
        bool
            If the record was deleted or not
    """
    if not tableName or not key or not val:
        return False

    try:
        res = ddb.Table(tableName).delete_item(
            Key = query
        )
        print(res)
        return True

    except client.exceptions.ResourceNotFoundException:
        print("Table does not exist")
        return False

    except Exception as e:
        print("Exception @ delete_record\n{}".format(e))
        return False

def check_active(tableName):
    """
    Function to check if a table is ACTIVE

    Params:
        tableName::str
            The table name to check
    Returns:
        bool
            If the table is active or not
    """
    if not tableName:
        return False

    try:
        if ddb.Table(tableName).table_status == "ACTIVE":
            return True
        return False

    except client.exceptions.ResourceNotFoundException:
        print("Table does not exist")
        return False

    except Exception as e:
        print("Exception @ check_status\n{}".format(e))
        return False