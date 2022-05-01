import serial
import rospy
from std_msgs.msg import String
from encoder import Encoder
import threading
import time
import port_finder
import os


class Comm():
    def __init__(self):
        self.PORT = '/dev/' + port_finder.find_usb("Xbee")
        #Port = '/dev/ttyUSB4' olarak kullanacagiz

        
        self.BAUD_RATE = 9600
        self.ser_mutex = threading.Lock()
        self.ser = serial.Serial(self.PORT, self.BAUD_RATE)
        
        rospy.init_node("comm_node", anonymous = True)
        self.data = []
        ############
        #Publishers#
        ############
        self.path_dir = os.path.join(os.getcwd(), "ground_control_station/team_imu/base/UAV")
        self.receive_pub = rospy.Publisher("/comm/rec", String, queue_size = 10)
        self.check_pub = rospy.Publisher("/monitor/check", String, queue_size = 10)
        self.data_publisher = rospy.Publisher("/ground_control", String, queue_size=10)

        #############
        #Subscribers#
        #############
        rospy.Subscriber("/comm/send_msg", String, self.send_message)
        rospy.Subscriber("/monitor/check_req", String, self.checker_send)
        rospy.Subscriber("/img/data", String, self.image_capture)

    def get_Xbee(self, port):
        while True:
            package = port.readline()
            rospy.loginfo("package:" + str(package))
	
            if len(package) is not 0:
                content = package.split('/')
                rospy.loginfo("XBEE Received Data:" + str(content[1]))
                self.received_message(content[1])
                with open(os.path.join(self.path_dir,"incoming_messages.txt"),'a') as f_lat_and_long:
		    
                    f_lat_and_long.write(str((content[1])))
                self.data_publisher.publish(str(content[1])) 


            rospy.sleep(1) #1 second  

    def send_message(self, msg):
        encoded = "/" + msg.data + "/" + "\n"
        rospy.loginfo('send_message:' + str(encoded))
        self.ser.write(encoded)

        

    def received_message(self, cont):
        msg = String()
        msg.data = cont
        self.receive_pub.publish(msg)
            

    def checker_send(self, msg):
        if msg is "Request":
            respon = String()
            respon.data = "comm"
            self.check_pub.publish(respon)

    def image_capture(self, msg):
        rospy.loginfo("Received image data")
        self.ser.write(msg.data + "\n")


if __name__ == "__main__":
    com = Comm()
    
    """readThrd = threading.Thread(target = com.get_Xbee, args=(com.ser, ))
    readThrd.start()"""
    com.get_Xbee(com.ser)

