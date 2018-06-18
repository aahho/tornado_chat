from db_handler import DBManager
import tornado.web, json
from utilities import utility, transformer
from slugify import slugify

class RenderHandler(tornado.web.RequestHandler):
	"""
	ClassName UserHandler
	It inherits RequestHandler class which routes incoming requests to handler
	This class is responsible for handling request related to User CRUD activity
	"""
	def set_default_headers(self):
		"""
		Method set_default_headers()
		To set default CORS Headers
		"""
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "*")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		self.set_header("Content-Type", "text/html; charset=UTF-8")

	@tornado.web.asynchronous ## For Non Blocking IO
	def get(self, method):
		"""
		Method get()
		To get user list OR by ID
		"""
		template = self.get_argument("template", None)
		channel = self.get_argument("channel", None)
		client = self.get_argument("client", None)
		if template is None:
			data = {
				'message' : 'Please Provide Valid Template Name!',
			}
			result = transformer.response_transform(data, status_code=400, message_type='error', message='Bad Request. Failed to respond', service_code='API_FAIL_004', hint='Please template name')
			self.set_status(400)
			self.write(json.dumps(result)) ## As it accepts only bytes, unicode, and dict objects
			self.finish()
		else:
			if channel is not None and client is not None:
				self.render("../templates/"+template+'.html', client_id=client, channel_id=channel)
			else:
				self.render("../templates/"+template+'.html')

	def options(self, method=None):
		"""
		Method options()
		For Option Call
		It doesnot contains any body
		"""
		self.set_status(204)
		self.finish()
