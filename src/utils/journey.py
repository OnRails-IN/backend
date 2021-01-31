import os
import json
import time
from elasticsearch import Elasticsearch, NotFoundError

from constants import ES_URI
ES = Elasticsearch([ ES_URI ])

def create_journey(ID, body):
	""" """
	# Required fields check
	if not ID or not body or not {'username', 'train_number', 'from'}.issubset(body):
		return False
	try:
		if 'timestamp' not in body:
			body['timestamp'] = int(time.time())
		if 'active' not in body:
			body['active'] = True
		
		global ES
		ES.index(index = "USER-JOURNEYS", id = ID, body = body)
		return True

	except Exception as e:
		print("Exception @ create_journey\n{}".format(e))
		return False

def list_journeys(includeInactive = False):
	""" """
	try:
		query = {} if includeInactive else { "active": True }

		global ES
		search = ES.search(query, index = "USER-JOURNEYS", _source = True)['hits']
		docs = [{ '_id': hit['_id'], **hit['_source'] } for hit in search['hits']]
		return json.loads(json.dumps({ 'total_docs': search['total']['value'], 'docs': docs }))

	except NotFoundError:
		return False

	except Exception as e:
		print("Exception @ list_journeys\n{}".format(e))
		return False


def get_journey(ID):
	""" """
	if not ID:
		return False
	try:
		global ES
		ref = ES.get(index = "USER-JOURNEYS", id = ID)
		return json.loads(json.dumps({'_id': ref['_id'], **ref['_source']}))

	except NotFoundError:
		return False

	except Exception as e:
		print("Exception @ get_journey\n{}".format(e))
		return False

def update_journey(ID, changes):
	""" """
	if not ID:
		return False
	try:
		if '_id' in changes:
			del changes['_id']
		
		changes['updated_timestamp'] = int(time.time())
		global ES
		body = ES.get(index = "USER-JOURNEYS", id = ID)['_source']
		body = {**body, **changes}
		ES.index(index = "USER-JOURNEYS", id = ID, body = body)
		return True

	except NotFoundError:
		return False

	except Exception as e:
		print("Exception @ update_journey\n{}".format(e))
		return False

def add_halt_to_journey(ID, haltObj):
	""" """
	if not ID:
		return False
	try:
		global ES
		body = ES.get(index = "USER-JOURNEYS", id = ID)['_source']
		
		if 'Halts' in body and haltObj not in body['Halts']:
			body['Halts'].append(haltObj)
		else:
			body['Halts'] = [haltObj]
		
		ES.index(index = "USER-JOURNEYS", id = ID, body = body)
		return True

	except NotFoundError:
		return False

	except Exception as e:
		print("Exception @ add_halt_to_journey\n{}".format(e))
		return False

def deactivate_journey(ID):
	""" """
	if not ID:
		return False
	try:
		global ES
		body = ES.get(index = "USER-JOURNEYS", id = ID)['_source']
		body['active'] = False
		ES.index(index = "USER-JOURNEYS", id = ID, body = body)
		return True

	except NotFoundError:
		return False

	except Exception as e:
		print("Exception @ deactivate_journey\n{}".format(e))
		return False