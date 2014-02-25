#!/usr/bin/env python

from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('settings.conf')

K = int(parser.get('algorithm', 'K'))

dbhost = parser.get('database', 'host')
dbname = parser.get('database', 'dbname')
dbuser = parser.get('database', 'user')
dbpass = parser.get('database', 'password')
dbtype = parser.get('database', 'dbtype')
dbitemtable = parser.get('database', 'itemtable')



