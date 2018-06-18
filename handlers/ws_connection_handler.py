from tornado import websocket
from channel_handler import ChannelDataHandler
import json

class WsConnectionHandler(websocket.WebSocketHandler):
	"""
	ClassName WsConnectionHandler
	It inherits WebSocketHandler class to establish web socket connection
	This class is responsible for handling web socket related activities like on_open, on_close, on_message
	"""

	def initialize(self, channel_handler):
		self.channel_data_handler = channel_handler

	def open(self, params):
		params = params.split('/')
		self.client_id = params[0]
		self.channel_id = params[1]
		self.channel_data_handler.set_client_channel_connection(self.client_id, self.channel_id, self)

	def on_message(self, message):
		data = json.loads(message)
		self.channel_data_handler.send_message(self.client_id, self.channel_id, data['msgtype'], data['payload'])

	def on_close(self):
		self.channel_data_handler.remove_client_channel_connection(self.client_id, self.channel_id)