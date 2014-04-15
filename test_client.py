#!/usr/bin/env python
"""Simple script for testing the server"""
import jsonrpclib
server = jsonrpclib.Server('http://localhost:8080')

# Add a user
uid = 1
server.add_user(uid)

# Print the rank of top 10 items for that user
result = server.get_rank(1)
print result

# Make a selection for the user (vid1 is preferred over vid2)
update_choice(vid1, vid2, uid)

# Now print the rank again
result = server.get_rank(1)
print result

