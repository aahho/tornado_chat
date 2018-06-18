import tornado.web, json
from db_handler import DBManager
from utilities import transformer
from channel_handler import ChannelHandler, ChannelDataHandler
from user_handler import UserHandler

class MainHandler(tornado.web.RequestHandler):
	"""
	ClassName MainHandler
	It inherits RequestHandler class which routes incoming requests to handlers
	In this hadler, methods gets called on the basis of request type
	"""
	
	def set_default_headers(self):
		"""
		Method set_default_headers()
		To set default CORS Headers
		"""
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with, access-token")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		self.set_header("Content-Type", "text/html; charset=UTF-8")

	def initialize(self):
		self.db_manager = DBManager('mongo')
		self.channel_data_handler = ChannelDataHandler()

	@tornado.web.asynchronous ## For Non Blocking IO
	def get(self):
		"""
		Method get()
		@param self
		Gets called on GET request method call
		"""
		channel_name = self.get_argument("channel", None)
		username = self.get_argument("username", None)

		if not channel_name or not username: ## If Channel Or User Not Provided, Render To Home Page
			self.render("../templates/index.html")
		else:
			channel = self.db_manager.retrieve(collection='channel', filter_by={'channel_name':channel_name})
			user = self.db_manager.retrieve(collection='users', filter_by={'username':username})
			if not len(channel) or not len(user):
				data = {
					'message' : 'Channel Or User Not Found !',
				}
				result = transformer.response_transform(data, status_code=404, message_type='error', message='Not Found. Failed to respond', service_code='API_FAIL_009', hint='Channel Or Username is Not Registered. Please Register First')
				self.set_status(404) ## For Setting Up HTTP Status Code
				self.write(json.dumps(result)) ## As it accepts only bytes, unicode, and dict objects
				self.finish()
			else:
				channel_id, client_id = self.channel_data_handler.attach_client_to_channel(channel[0]['id'], user[0]['id'])
				data = {
					'channel_id' : channel_id,
					'client_id' : client_id
				}
				result = transformer.response_transform(data, status_code=200, message_type='success', message='Successfully Responded', service_code='API_SUCCESS_014', hint='Channel and Client Found')
				self.set_header("Content-Type", "application/json")
				self.set_status(200) ## For Setting Up HTTP Status Code
				self.write(json.dumps(result)) ## As it accepts only bytes, unicode, and dict objects
				self.finish()
				# self.render("../templates/chat.html", client_id=client_id, channel_id=channel_id)

	@tornado.web.asynchronous ## For Non Blocking IO
	def post(self):
		self.set_header("Content-Type", "text/plain")
		self.write("You wrote " + self.get_body_argument("message"))
		self.finish()