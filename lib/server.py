#!/usr/bin/env python

from SocketServer import ThreadingMixIn
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import time
from api import *

"""JSON-RPC Server module

	This is just a simple threaded server that handles all
	the JSON-RPC responses. 
"""

# Make sure a new thread is spawned when a reqest is coming in.
class SimpleThreadedJSONRPCServer(ThreadingMixIn, SimpleJSONRPCServer):
		pass

def start_server():
	# Register API functions
	server = SimpleThreadedJSONRPCServer(('localhost', 8080))
	server.register_function(add_user)
	server.register_function(update_choice)
	server.register_function(get_rank)
	server.register_function(get_random_pair)
	server.serve_forever()

if __name__ == '__main__':
	start_server()
