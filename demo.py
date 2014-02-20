#!/usr/bin/env python

import init_db()
from ConfigParser import SafeConfigParser
import psycopg2
import sys
import pprint

def init_db()
    setup_db()
    parser = SafeConfigParser()
    parser.read('settings.conf')

    K = int(parser.get('algorithm', 'K'))

    conn_string = "host='" + parser.get('database', 'host') + "' dbname='" + parser.get('database', 'dbname') + "' user='" + parser.get('database', 'user') + "' password='" + parser.get('database', 'password') + "'" 
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    val_string = ""
    for i in xrange(K): val_string += "val" + str(i) + " NUMERIC DEFAULT 0, "
    create_umat = ("DROP TABLE IF EXISTS umat;"
                    "CREATE TABLE umat ("
                        "id SERIAL NOT NULL PRIMARY KEY,"
                        "uid integer NOT NULL," + 
                        val_string[:-2] + 
                    ");")
    
    create_umat = ("DROP TABLE IF EXISTS vmat;"
                    "CREATE TABLE vmat ("
                        "id SERIAL NOT NULL PRIMARY KEY,"
                        "vid integer NOT NULL," + 
                        val_string[:-2] + 
                    ");")
    
    cursor.execute(create_umat)
    cursor.execute("insert into umat (uid, val1) values (1,2);")
    cursor.execute("SELECT * FROM umat")
    records = cursor.fetchall()
    
def populate_data()
__name__ == '__main__':
    init_db()
    populate_data

