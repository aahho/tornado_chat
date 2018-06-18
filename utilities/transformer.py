import json

def user_transform(user):
	data = {
		'id' : user['id'] if 'id' in user else None,
		'username' : user['username'],
		'display_name' : user['display_name'],
		'created_at' : str(user['created_at']),
		'updated_at' : str(user['updated_at']),
	}
	return data

def channel_transform(channel):
	data = {
		'id' : channel['id'],
		'name' : channel['channel_name'] if 'channel_name' in channel else channel['name'],
		'created_at' : str(channel['created_at']) if 'created_at' in channel else None,
		'updated_at' : str(channel['updated_at']) if 'updated_at' in channel else None,
	}
	return data

def message_transform(user, channel, message_type, payload):
	data = {
		'message' : {
			'type' : message_type,
			'payload' : payload
		},
		'user' : {
			'username' : user['username'],
			'display_name' : user['display_name'],
			'id' : user['id'],
			'created_at' : user['created_at']
		}
	}
	return json.dumps(data)

def response_transform(data, status_code=200, message_type='success', message='Successfully Responded', service_code='API_SUCCESS_001', hint='Success'):
	response = {
		'data' : data,
		'notification' : {
			'type' : message_type,
			'status' : status_code,
			'service_code' : service_code,
			'message' : message,
			'hint' : hint,
			'count' : len(data) if type(data) == type([]) else 1
		}
	}
	return response