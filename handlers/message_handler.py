from db_handler import DBManager
import tornado.web, json
from utilities import utility, transformer

class MessageHandler(tornado.web.RequestHandler):
	"""
	ClassName MessageHandler
	It inherits RequestHandler class which routes incoming requests to handler
	This class is responsible for handling request related to Message Fetching activity
	"""
	def set_default_headers(self):
		"""
		Method set_default_headers()
		To set default CORS Headers
		"""
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with, access-token")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		self.set_header("Content-Type", "application/json")

	def initialize(self):
		self.db_manager = DBManager('mongo')

	@tornado.web.asynchronous ## For Non Blocking IO
	def get(self, method):
		"""
		Method get()
		To get user list OR by ID
		"""
		channel_name = self.get_argument("name", '')
		channels = self.db_manager.retrieve(collection='channel', filter_by={'channel_name':channel_name})
		if not len(channels):
			data = {
				'message' : 'Channel Not Found !',
			}
			result = transformer.response_transform(data, status_code=404, message_type='error', message='Not Found. Failed to respond', service_code='API_FAIL_010', hint='Channel name should be registered first')
			self.set_status(404)
		else:
			messages = self.db_manager.retrieve(collection='channel_message__'+channels[0]['channel_name'], filter_by={})
			result = transformer.response_transform([message for message in messages])
			self.set_status(200)
		self.write(json.dumps(result)) ## As it accepts only bytes, unicode, and dict objects
		self.finish()

	def options(self):
		"""
		Method options()
		For Option Call
		It doesnot contains any body
		"""
		self.set_status(204)
		self.finish()
