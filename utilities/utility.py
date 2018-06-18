import uuid, datetime

def generate_uuid():
	"""
	Returns a unique ID
	"""
	return uuid.uuid4()

def get_date_time():
	"""
	Returns Current Date Time
	"""
	return datetime.datetime.now()