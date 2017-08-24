#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sqlite3
import os
import sys
import re
import urllib2
import ipset


date=datetime.datetime.now()
print date.strftime("%Y-%m-%d")

inurl = 'https://raw.githubusercontent.com/zapret-info/z-i/master/dump.csv'
infile = ''
dbfile = 'hosts.db'
listname = 'roskomfuckoff'


def createdb(dbfile):
	db = sqlite3.connect(dbfile)
	db.text_factory = str
	c = db.cursor()
	c.execute('CREATE TABLE imported_list (ipaddr varchar unique, hostname, date)')
	c.execute('CREATE TABLE userlist (ipaddr, hostname, date)')
	db.close()
	sys.exit(0)

def dbadd(table,ip,host,date):
	c= db.cursor()
	c.execute("INSERT OR IGNORE INTO "+table+" VALUES (?, ?, ?)", (ip, host, date))


def add_ip(table,ip):
	c= db.cursor()
	for row in c.execute('SELECT * FROM '+table+''):
		record = row[0].split(',')
		for i in record:
			ipset.ipset_add_ip(listname,i)

	
	
def parser(string):
	ip = []
	data = string.rstrip('\n').split(';')
	rawip = data[0].split(' | ')
	for i in rawip:
		if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",i):
			ip.append(i)
	ip = ','.join(ip)
	host = ''.join(data[1:2]).decode('cp1251').encode('utf8')
	date = ''.join(data[5::]).split('-')
	date = '.'.join(date[::-1])
	return (ip, host, date)

def dbinfill(data):
	for row in data:
		record = parser(row)
		if record[0] == '' and record[1] == '' and record[2] == '':
			pass
		elif record[0] == '':
			print record[1]
		elif record[1] == '':
			dbadd("imported_list",record[0],'0',record[2])
		else:
			dbadd("imported_list",record[0],record[1],record[2])
	db.commit()

if os.path.isfile(dbfile):
	if os.access(dbfile, os.W_OK):
		db = sqlite3.connect(dbfile)
		db.text_factory = str
	else:
		print "Unable to open database for write"
else:
	print "Database not found. Creating new one!"
	createdb(dbfile)	

if '-f' in list(sys.argv[1:]):
	if infile == '':
		print "Downloading and infilling database"
		response = urllib2.urlopen(inurl)
		blocklist = response.read()
		tf = open('dump.csv', 'w')
		for row in blocklist:
			tf.write(row)
		with open('dump.csv', 'r') as blocklist:
			dbinfill(blocklist)
	else:
		with open(infile, 'r') as blocklist:
			dbinfill(blocklist)
	db.close()
			
elif '-g' in list(sys.argv[1:]):
	print "Adding IPs from database to ipset"
	ipset.ipset_flush_set(listname)
	add_ip("imported_list",listname)
	db.close()
else:
	print "Use one of two options:"
	print "'generate' or 'fetch' (-g or -f)"
