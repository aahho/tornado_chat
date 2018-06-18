from db_handler import DBManager
import tornado.web, json
from utilities import utility, transformer
from slugify import slugify

class ChannelHandler(tornado.web.RequestHandler):
	"""
	ClassName ChannelHandler
	This class is used for creating/deleting channel and adding/removing client connection
	"""
	
	def set_default_headers(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "*")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		self.set_header("Content-Type", "application/json")
	
	def initialize(self):
		self.db_manager = DBManager('mongo')
	
	@tornado.web.asynchronous
	def get(self, method):
		"""
		Method get()
		To get channel list OR by ID
		"""
		channel_name = self.get_argument("channel", None)
		if channel_name is None:
			channels = self.db_manager.list(collection='channel')[::-1]
		else:
			channels = self.db_manager.retrieve(collection='channel', filter_by={'channel_name':channel_name})
		result = transformer.response_transform([transformer.channel_transform(channel) for channel in channels])
		self.write(json.dumps(result)) ## As it accepts only bytes, unicode, and dict objects
		self.set_status(200)
		self.finish()

	@tornado.web.asynchronous
	def post(self, method):
		"""
		Method post()
		To register a channel
		"""
		data = json.loads(self.request.body)
		channel_name = data['name'] if 'name' in data else ''
		if channel_name == '' or len(channel_name) < 5:
			data = {
				'message' : 'Please Provide Valid Channel Name !',
			}
			result = transformer.response_transform(data, status_code=400, message_type='error', message='Bad Request. Failed to respond', service_code='API_FAIL_001', hint='Channel name should be more than 4 words')
			self.set_status(400)
		else:
			channels = self.db_manager.retrieve(collection='channel', filter_by={'channel_name':slugify(channel_name, max_length=30, word_boundary=True, save_order=True)})
			if len(channels):
				data = {
					'message' : 'Channel Name Already Exists !',
				}
				result = transformer.response_transform(data, status_code=409, message_type='error', message='Duplicate Entry. Failed to respond', service_code='API_FAIL_002', hint='Try with different channel name')
				self.set_status(409)
			else:
				data = {
					'_id' : str(utility.generate_uuid()),
					'id' : str(utility.generate_uuid()),
					'channel_name' : slugify(channel_name, max_length=30, word_boundary=True, save_order=True),
					'created_at' : str(utility.get_date_time()),
					'updated_at' : str(utility.get_date_time()),
				}
				channel = self.db_manager.create(collection='channel', data=data)
				if channel:
					del data['_id']
					result = transformer.response_transform(data, status_code=201, service_code='API_SUCCESS_001', hint='Channel Added Successfully')
					self.set_status(201)
				else:
					data = {
						'message' : 'Failed To Register Channel. Try Again !',
					}
					result = transformer.response_transform(data, status_code=500, message_type='error', message='Something Went Wrong', service_code='API_FAIL_003', hint='We messed up !')
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

class ChannelDataHandler(object):

	def __init__(self):
		self.db_manager = DBManager('mongo')
		self.channel_users = {}

	def attach_client_to_channel(self, channel_id, client_id):
		client_channel = self.db_manager.retrieve(collection='channel_client', filter_by={'channel_id':channel_id, 'client_id':client_id})
		if not len(client_channel):
			data = {
				'_id' : str(utility.generate_uuid()),
				'id' : str(utility.generate_uuid()),
				'channel_id' : channel_id,
				'client_id' : client_id,
				'created_at' : str(utility.get_date_time()),
				'updated_at' : str(utility.get_date_time()),
			}
			self.db_manager.create(collection='channel_client', data=data)
		return channel_id, client_id

	def set_client_channel_connection(self, client_id, channel_id, ws_connection):
		if channel_id not in self.channel_users:
			self.channel_users[channel_id] = {}
		if client_id not in self.channel_users[channel_id]:
			self.channel_users[channel_id][client_id] = ws_connection
			self.send_pong_on_join(client_id, channel_id)
		
	def send_pong_on_join(self, client_id, channel_id):
		return self.send_message(client_id, channel_id, 'join', 'Joined the Channel')

	def send_pong_on_leave(self, client_id, channel_id):
		return self.send_message(client_id, channel_id, 'leave', 'Left the Channel')

	def send_message(self, client_id, channel_id, message_type, payload):
		user = self.db_manager.retrieve(collection='users', filter_by={'id':client_id})[0]
		channel = self.db_manager.retrieve(collection='channel', filter_by={'id':channel_id})[0]
		data = transformer.message_transform(user=user, channel=channel, message_type=message_type, payload=payload)

		message = json.loads(data)
		message['_id'] = str(utility.generate_uuid())
		message['id'] = str(utility.generate_uuid())
		message['created_at'] = str(utility.get_date_time())
		message['updated_at'] = str(utility.get_date_time())
		self.db_manager.create(collection='channel_message__'+channel['channel_name'], data=message)
		
		for client in self.channel_users[channel_id]:
			self.channel_users[channel_id][client].write_message(data)

	def remove_client_channel_connection(self, client_id, channel_id):
		if channel_id in self.channel_users and client_id in self.channel_users[channel_id]:
			del self.channel_users[channel_id][client_id]
		return self.send_pong_on_leave(client_id, channel_id)
