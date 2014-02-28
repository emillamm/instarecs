#!/usr/bin/env python

from ConfigParser import SafeConfigParser
import decimal

parser = SafeConfigParser()
parser.read('settings.conf')

K = int(parser.get('algorithm', 'K'))
alpha = decimal.Decimal(parser.get('algorithm', 'alpha'))
lambd = decimal.Decimal(parser.get('algorithm', 'lambda'))


dbhost = parser.get('database', 'host')
dbname = parser.get('database', 'dbname')
dbuser = parser.get('database', 'user')
dbpass = parser.get('database', 'password')
dbtype = parser.get('database', 'dbtype')
itemtable = parser.get('database', 'itemtable')


