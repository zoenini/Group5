#!/usr/bin/python
#c = 0
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
from time import sleep
import time

from pox.lib.packet.ethernet import ethernet
import os
import csv
import sys

counter = 0
def static_num():
	global counter
	counter=counter+1
	return counter




policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

table = []
with open('/home/mininet/pox/pox/misc/firewall-policies.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		table.append(row)
		

policyFile = "%s/pox/pox/misc/counter.csv" % os.environ[ 'HOME' ]

table1 = []
with open('/home/mininet/pox/pox/misc/counter.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		table1.append(row)


policyFile = "%s/pox/pox/misc/blockpolicy.csv" % os.environ['HOME']

table2 = []
with open('/home/mininet/pox/pox/misc/blockpolicy.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		table2.append(row)



print "How many time to connect"
timeCounter = input()
print "*******"
print timeCounter
print "*******"

print "Which connection to setup block between"
first = raw_input()
second = raw_input()

table1[1][1] = first
table1[1][2] = second


dict_table = {EthAddr(table[1][1]) : EthAddr(table[1][2]), EthAddr(table[1][2]) : EthAddr(table[1][1])}

	
if len(table)>2:
		
	for i in range(2, 3):
		dict1 = {EthAddr(table[i][1]) : EthAddr(table[i][2]), EthAddr(table[i][2]) : EthAddr(table[i][1])}
		dict_table.update(dict1)
			
dict_table1 = {EthAddr(table1[1][1]) : EthAddr(table1[1][2]), EthAddr(table1[1][2]) : EthAddr(table1[1][1])}
	
if len(table1)>2:
		
	for i in range(2, 3):
		dict11 = {EthAddr(table1[i][1]) : EthAddr(table1[i][2]), EthAddr(table1[i][2]) : EthAddr(table1[i][1])}
		dict_table1.update(dict11)
			
dict_table2 = {EthAddr(table2[1][1]) : EthAddr(table2[1][2]), EthAddr(table2[1][2]) : EthAddr(table2[1][1])}	
	
if len(table2)>2:
	for i in range(2, len(table2)):
	
		dict3 = {EthAddr(table2[i][1]) : EthAddr(table2[i][2]), EthAddr(table2[i][2]) : EthAddr(table2[i][1])}
		dict_table2.update(dict3)
		
print "dict_table"
print table1[1][1]
print table1[1][2]
print dict_table
print "***********"		
	

log = core.getLogger()

d = static_num()


	
	
def timeCompare():
	h1 = time.strftime("%H")
	m1 = time.strftime("%M")
	#print ("time", h1, ":",m1)
	h2 = '08'
	m2 = '30'
	h3 = '18'
	m3 = '30'
	if h1>h2 and h1<h3:
		return 1
	if h1==h2:
		if m1>m2:
			return 1
	if h1==h3:
		if m1<m3:
			return 1
	return 0
	

class FireWall (object):
	def __init__ (self, connection):
		self.connection = connection
		connection.addListeners(self)
	

	def _handle_PacketIn (self, event):
		packet = event.parsed
		def drop ():
			
			msg = of.ofp_flow_mod()
			msg.priority = 1000
			msg.match.dl_src = packet.src
			msg.match.dl_dst = packet.dst
		
			self.connection.send(msg)
	
		if packet.src in dict_table:
			if dict_table[packet.src] == packet.dst:
				log.debug("Droping flow %s->%s", packet.src, packet.dst)
				drop()
		d = static_num()
		print"***d = "
		print d
		print "******"
		if d>timeCounter:
			if packet.src in dict_table1:
				if dict_table1[packet.src] == packet.dst:
					
						log.debug("Droping flow %s->%s", packet.src, packet.dst)
						drop()
		if packet.src in dict_table2:
			timeCond = timeCompare()
			if timeCond == 0:	
				print "****HERE*****"
				if dict_table2[packet.src] == packet.dst:
				
					log.debug("Droping flow %s->%s", packet.src, packet.dst)
					drop()		
class Firewall (EventMixin):

	def __init__ (self):
		core.openflow.addListeners(self)
        log.debug("Enabling Firewall Module")

	def _handle_ConnectionUp (self, event):
		log.debug("Switch %s has come up", dpidToStr(event.dpid))
		FireWall(event.connection)


def launch ():

	core.registerNew(Firewall)
