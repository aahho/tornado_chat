class MongoDBWrapper(object):
	"""
	ClassName MongoDBWrapper
	For performing CRUD operation on MongoDB
	MongoDB is a NoSQL Database where we create collections to store relevant data
	"""
	def __init__(self):
		super(MongoDBWrapper, self).__init__()

	def store(self, collection, data):
		return collection.insert_one(data)

	def all(self, collection):
		return collection.find()

	def retrieve(self, collection, filter_by):
		return list(collection.find(filter_by))

	def push(self, collection, data, filter_by):
		return collection.update(filter_by, {'$push': data})

	def update_single(self, collection, data, filter_by):
		return collection.update_one(filter_by, {'$set': data})