#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 18:19:06 2017

@author: EscobarWest
"""

import time
import datetime
import sqlite3
import requests
from requests.exceptions import ConnectionError


conn = sqlite3.connect('cryptocurrencies.db', detect_types=sqlite3.PARSE_DECLTYPES)
c = conn.cursor()

if False: # Don't run this statement unless you want to delete the table    
    c.execute('DROP TABLE XXBTZUSD')
    c.execute('''CREATE TABLE XXBTZUSD
                  (date INT PRIMARY KEY,
                  price REAL,
                  volume REAL)''')

url = 'https://api.kraken.com/0/public/OHLC?pair=XXBTZUSD'

while(1):
    try:
        raw_data = requests.get(url)
        
        result = raw_data.json()['result']['XXBTZUSD'][:-1]
        result_iter = ((row[0],row[4],row[6]) for row in result)
        
        c.executemany('INSERT OR IGNORE INTO XXBTZUSD VALUES (?,?,?)', result_iter)
        conn.commit()
        
        print('{}: committed new entries. Now sleeping...'
              .format(datetime.datetime.fromtimestamp(time.time())))
        time.sleep(3600)
    except ConnectionError:
        print('{}: Could not connect to internet. Retrying in 1 minute...'
              .format(datetime.datetime.fromtimestamp(time.time())))
        time.sleep(60)
