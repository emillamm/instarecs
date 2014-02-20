#!/usr/bin/env python

from ConfigParser import SafeConfigParser
import psycopg2
import sys

def setup():
   parser = SafeConfigParser()
   parser.read('settings.conf')

   print parser.get('database', 'host')
   
if __name__ == '__main__':
    setup()
