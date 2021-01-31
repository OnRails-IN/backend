import os
import json
import time
from elasticsearch import Elasticsearch, NotFoundError

from constants import ES_URI
ES = Elasticsearch([ ES_URI ])

def create_spotting(ID, body):
	""" """
	if not ID or not {'username', 'spotting_category'}.issubset(body):
		return False
	try:
		if 'timestamp' not in body:
			body['timestamp'] = int(time.time())
		if 'active' not in body:
			body['active'] = True

		ES.index(index = "USER-SPOTTINGS", id = ID, body = body)
		return True

	except Exception as e:
		print("Exception @ create_spotting\n{}".format(e))
		return False

def list_spottings(includeInactive = False):
	""" """
	try:
		query = {} if includeInactive else { "active": True }
		ES.search(query, index = "USER-SPOTTINGS", source = True)['hits']
		docs = [{ '_id': hit['_id'], **hit['_source'] } for hit in search['hits']]
		return json.loads(json.dumps({ 'total_docs': search['total']['value'], 'docs': docs }))

	except NotFoundError:
		return False

	except Exception as e:
		print("Exception @ list_spottings\n{}".format(e))
		return False

def get_spotting(ID):
	""" """
	if not ID:
		return False
	try:
		ref = ES.get(index = "USER-SPOTTINGS", id = ID)
		return json.loads(json.dumps({ '_id': ref['_id'], **ref['_source'] }))

	except NotFoundError:
		return False

	except Exception as e:
		print("Exception @ get_spotting_by_id\n{}".format(e))
		return False

def update_spotting(ID, changes):
	""" """
	if not ID:
		return False
	try:
		if '_id' in changes:
			del changes['_id']

		changes['updated_timestamp'] = int(time.time())
		body = ES.get(index = "USER-SPOTTINGS", id = ID)['_source']
		body = {**body, **changes}
		ES.index(index = "USER-SPOTTINGS", id = ID, body = body)
		return True

	except NotFoundError:
		return False

	except Exception as e:
		print("Exception @ update_spotting\n{}".format(e))
		return False

def deactivate_spotting(ID):
	""" """
	if not ID:
		return False
	try:
		global ES
		body = ES.get(index = "USER-SPOTTINGS", id = ID)['_source']
		body['active'] = False
		ES.index(index = "USER-SPOTTINGS", id = ID, body = body)
		return True

	except NotFoundError:
		return False

	except Exception as e:
		print("Exception @ deactivate_spotting\n{}".format(e))
		return False