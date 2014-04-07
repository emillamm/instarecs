#!/usr/bin/env python

from SocketServer import ThreadingMixIn
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import time
from api import *


class SimpleThreadedJSONRPCServer(ThreadingMixIn, SimpleJSONRPCServer):
	pass
    

server = SimpleThreadedJSONRPCServer(('localhost', 8080))
server.register_function(add_user)
server.register_function(update_choice)
server.register_function(get_rank)
server.register_function(get_random_pair)
server.serve_forever()

