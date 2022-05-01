#!/usr/bin/env python

import rospy
from std_msgs.msg import String

import threading
import serial

import time

import json

#import redis

import time
import datetime

import sys

from cryptography.fernet import Fernet

key = 'VOt7mKQZuOwOHhocS7WA_MbXvB0GsDuCY6Q2Kd1xF7E='
f = Fernet(key)

global connected
connected = False

global ser_mutex
ser_mutex = threading.Lock()

#global r
#r = redis.Redis()


def encode_package(message):
    return '##<' + str(MY_IP) + '<' + message + '<**<'


def decode_package(package):
    pck_split = [x.strip() for x in package.split('<')]
    return pck_split


def send_package(package):
    #ser = serial.Serial(MY_PORT, MY_BAUD)
    global ser_mutex
    global serial_port
    ser_mutex.acquire()    
    serial_port.write(package)
    ser_mutex.release()
    #ser.close()

def handle_data(inputData):
    #global r
    #print(inputData + '\n')
    file = open('incoming_messages.txt','a',0)
    print("---------------")
    ts = time.time()
    time_curr= datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    msg = String()
    try:
        msg.data = f.decrypt(str(inputData))
        print("received message in callback: ", msg.data)
        file.write(time_curr+" "+msg.data+"\n") 
    #received_message_pub.publish(msg)
    #r.rpush('incoming_messages', time_curr +" " + msg.data + "\n")
        print("---------------")
    except:
        msg.data = ""
		print("received message in callback: ", msg.data)
        file.write(time_curr+" "+msg.data+"\n") 
    file.close()
def read_from_port(ser):
	global ser_mutex
	global connected
	while not connected:
		#serin = ser.read()
		connected = True

		data_string = ''
		while True:
                   #try:
			ser_mutex.acquire()
		
			reading = ser.readline().decode()
						
			#reading_ = ser.readline()		
			#if len(reading_)>0:
			#	print("raw reading: ", reading_)
			#	if isinstance(reading_,basestring):
			#		print("string")	
			#reading= reading_.decode()
			ser_mutex.release()
			
			if len(reading) > 0:
				data_string = data_string + reading
				#print("before checking **, ", data_string)
				#data_string = f.decrypt(data_string.encode())
				data_split = decode_package(data_string)
				if '**' in data_split:
					last_idx = data_split.index('**')
					package_split = data_split[0:last_idx+1]
					#print("package_split: ", package_split)
					if package_split[0] == '':
						del package_split[0]
					#package = ', '.join(package_split)
					if package_split[1] == MY_IP:
						package = package_split[2]#'='.join(package_split[2:4])
						handle_data(package)
					package_remaining = data_split[last_idx+1:len(data_split)]
					data_string = '<'.join(package_remaining)
		   #except expression:
			#time.sleep(0.2)
                        #sys.exit(0)
                        #exit()
			


def callback_send_command(msg):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", msg.data)
    print("callback_send_command:", msg.data)
    # outGoingConn[0].send(data.data)  # echo
    pck = encode_package(msg.data)
    send_package(pck)



def load_config_data():
	global MY_ID
	global MY_PORT
	global MY_BAUD
	global MY_IP

	configFile = open('configFile.json', 'r')
	configData = json.load(configFile)

	MY_ID = str(configData['my_id'])
	print "MY ID: ", MY_ID
	MY_PORT = str(configData['my_port'])
	print "MY PORT: ", MY_PORT
	MY_BAUD = int(configData['my_baud'])
	MY_IP = str(configData['my_ip'])

###### main #########

load_config_data()

rospy.init_node("comm_ground")

rospy.Subscriber('/mrs/send_command', String, callback_send_command)

# rospy.Subscriber('/mrs/send_message', String, callback_send_message)

received_message_pub = rospy.Publisher('/mrs/received_message', String, queue_size=10)

threads = []

print("Ready to broadcast!")
print("-------------------++<>++-----------------------")


serial_port = serial.Serial(MY_PORT, MY_BAUD, timeout=0)
thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.start()


rate = rospy.Rate(10)  # 10hz
while not rospy.is_shutdown():
    # do publishing
    # pub.publish(msg)
    rate.sleep()
