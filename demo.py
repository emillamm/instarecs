#!/usr/bin/env python
from lib import fields
from lib import init_db
from lib import server
"""Demo for trying out instarecs using a small IMDB dataset"""

# Initialize feature vectors for each movie
init_db.populate_data()

# Run the server
server.start_server()