#!/usr/bin/env python

import jsonrpclib
server = jsonrpclib.Server('http://localhost:8080')
result = server.add_user(123)
print result
result = server.get_rank(1)
print result

