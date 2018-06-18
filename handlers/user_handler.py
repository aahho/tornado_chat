from db_handler import DBManager
import tornado.web, json
from utilities import utility, transformer
from slugify import slugify

class UserHandler(tornado.web.RequestHandler):
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
		self.set_header("Content-Type", "application/json")

	def initialize(self):
		self.db_manager = DBManager('mongo')

	@tornado.web.asynchronous ## For Non Blocking IO
	def get(self, method):
		"""
		Method get()
		To get user list OR by ID
		"""
		username = self.get_argument("username", None)
		if username is None:
			users = self.db_manager.list(collection='users')[::-1]
		else:
			users = self.db_manager.retrieve(collection='users', filter_by={'username':username})
		
		result = transformer.response_transform([transformer.user_transform(user) for user in users])
		self.set_status(200)
		self.write(json.dumps(result)) ## As it accepts only bytes, unicode, and dict objects
		self.finish()

	@tornado.web.asynchronous ## For Non Blocking IO
	def post(self, method):
		"""
		Method post()
		To add a user to db record
		"""
		data = json.loads(self.request.body)
		username = data['username'] if 'username' in data else ''
		display_name = data['display_name'] if 'display_name' in data else ''
		
		if username == '' or display_name == '':
			data = {
				'message' : 'Please Provide Valid Username and Display Name !',
			}
			result = transformer.response_transform(data, status_code=400, message_type='error', message='Bad Request. Failed to respond', service_code='API_FAIL_004', hint='Username and Display Name is Required')
			self.set_status(400)
		else:
			users = self.db_manager.retrieve(collection='users', filter_by={'username':slugify(username, max_length=30, word_boundary=True, save_order=True)})
			if len(users):
				data = {
					'message' : 'Username Already Taken !',
				}
				result = transformer.response_transform(data, status_code=409, message_type='error', message='Duplicate Entry. Failed to respond', service_code='API_FAIL_002', hint='Try with different username')
				self.set_status(409)
			else:
				data = {
					'_id' : str(utility.generate_uuid()),
					'id' : str(utility.generate_uuid()),
					'username' : slugify(username, max_length=30, word_boundary=True, save_order=True),
					'display_name' : display_name,
					'created_at' : str(utility.get_date_time()),
					'updated_at' : str(utility.get_date_time()),
				}
				user = self.db_manager.create(collection='users', data=data)
				if user:
					del data['_id']
					result = transformer.response_transform(data, status_code=201, service_code='API_SUCCESS_003', hint='User Added Successfully')
					self.set_status(201)
				else:
					data = {
						'message' : 'Failed To Register User. Try Again !',
					}
					result = transformer.response_transform(data, status_code=500, message_type='error', message='Something Went Wrong', service_code='API_FAIL_006', hint='We messed up !')
					self.set_status(500)
		self.write(json.dumps(result))
		self.finish()

	def options(self, method=None):
		"""
		Method options()
		For Option Call
		It doesnot contains any body
		"""
		self.set_status(204)
		self.finish()
