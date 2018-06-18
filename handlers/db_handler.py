import config, importlib
from utilities import utility

class DBManager(object):
	"""
	ClassName DBHandler
	For making DB queries and storing it in database
	@param connection - Name of the connection in use
	"""
	def __init__(self, connection_name):
		super(DBManager, self).__init__()
		self.connection = config.DATABASES[connection_name]['ENGINE']
		self.database = self.connection[config.DATABASES[connection_name]['NAME']]
		self.wrapper = config.DATABASES[connection_name]['WRAPPER']
		
	def list(self, collection):
		collection = self.database[collection]
		result = list(self.wrapper.all(collection))
		return result

	def retrieve(self, collection, filter_by):
		collection = self.database[collection]
		result = self.wrapper.retrieve(collection, filter_by)
		return result

	def create(self, collection, data):
		collection = self.database[collection]
		return self.wrapper.store(collection, data)

	def push(self, collection, data, filter_by):
		collection = self.database[collection]
		return self.wrapper.push(collection, data, filter_by)

	def update_single(self, collection, data, filter_by):
		collection = self.database[collection]
		return self.wrapper.update_single(collection, data, filter_by)
