import tornado.ioloop, tornado.web, os, env, sys
from handlers import main_handler, channel_handler, user_handler, ws_connection_handler, message_handler, view_handler

def main():
	channel = channel_handler.ChannelDataHandler()
	return tornado.web.Application(
			[
				(r"/", main_handler.MainHandler),
				(r"/view/(.*)", view_handler.RenderHandler),
				(r"/channel/(.*)", channel_handler.ChannelHandler), ## It accepts all requests related to a channel
				(r"/user/(.*)", user_handler.UserHandler), ## It accepts all requests related to a channel
				(r"/message/(.*)", message_handler.MessageHandler), ## It accepts all requests related to a channel
				(r"/ws/(.*)", ws_connection_handler.WsConnectionHandler, {'channel_handler': channel}),
			],
			debug=env.DEBUG,
			static_path=os.path.join(os.path.dirname(__file__), "static")
		)

if __name__ == '__main__':
	args = sys.argv
	app = main() ## This function is used to start the server
	if len(args) > 1:
		port = int(args[1])
	else:
		port = 8080
	app.listen(8080, '192.168.5.124')
	print "\n Starting Up Server On Port "+str(port)+" \n\n GoTo url http://127.0.0.1:"+str(port)+" ... \n"
	tornado.ioloop.IOLoop.current().start()