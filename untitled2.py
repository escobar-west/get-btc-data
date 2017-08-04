# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 16:39:32 2017

@author: victor.suriel
"""
import time
import datetime
import sqlite3
import requests


conn = sqlite3.connect('example.db', detect_types=sqlite3.PARSE_DECLTYPES)
c = conn.cursor()

if True: # Don't run this statement unless you want to delete the table    
    c.execute('DROP TABLE btc')
    c.execute('CREATE TABLE btc (date timestamp, price real)')

url = 'https://www.bitstamp.net/api/ticker/'

for _ in range(5):
    raw_data = requests.get(url)
    price = raw_data.json()['last']
    
    c.execute('INSERT INTO btc VALUES (?,?)', (datetime.datetime.today(), price))
    print('inserted values into table')
    conn.commit()
    time.sleep(3)
    
for row in c.execute('SELECT * FROM btc'):
    print(row)