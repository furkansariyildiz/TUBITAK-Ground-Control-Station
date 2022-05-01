import rospy
from std_msgs.msg import String, Float32MultiArray
from geometry_msgs.msg import Vector3Stamped
import threading
import time
#from gps_common.msg import GPSFix
#from gps_common.msg import GPSStatus
from sensor_msgs.msg import NavSatFix
import numpy as np
import math
import json
import os



class CommPort():
    def __init__(self):
        rospy.init_node("comm_port", anonymous=False)

        self.data = []
        self.file = []
        ############
        #Publishers#
        ###########

        self.data_publisher = rospy.Publisher("/ground_control", String, queue_size=10)
        self.json_publisher = rospy.Publisher("/data_from_vehicle", String, queue_size=10)

        self.lat = None
        self.lon = None
        self.altitude = None
        self.bar_height = None

        """"
        Duruma bagli olarak eklenebilir
        self.time = None
        self.connected_status = None
        self.arm_status = None
        self.guided_status = None
        self.mode = None
        """


        self.x_speed = None
        self.y_speed = None
        self.z_speed = None


        self.roll = None
        self.pitch = None
        self.yaw = None
        self.heading = None

        self.battery = None
        
        self.splitted_data = None

        self.json_data = {}
        self.json_data_str = ""

    def get_Xbee(self):
        folder_name = os.path.join(os.getcwd(), 'team_imu/base')
        folder_name_UAV = os.path.join(folder_name, 'UAV')
        
        for file_name in os.listdir(folder_name_UAV):
            if file_name.endswith("yalanci_data.txt"):
                self.file = os.path.join(folder_name_UAV, file_name)
                print(self.file)
        while not rospy.is_shutdown(): 
            try:
                with open(self.file, 'r') as f:
                    data = f.read().splitlines(True)
                    self.splitted_data = data[0].split(" ")
                    self.lat = float(self.splitted_data[5])
                    self.lon = float(self.splitted_data[7].split(";")[0])
                    self.altitude = float(self.splitted_data[12].split(";")[1])
                    
                    self.heading = float((self.splitted_data[17].split(";")[1]).split(":")[1])
                    self.roll = float(self.splitted_data[13])
                    self.pitch = float(self.splitted_data[15])
                    self.yaw = float(self.splitted_data[17].split(";")[0])
                    
                    self.speed_x = float(self.splitted_data[8])
                    self.speed_y = float(self.splitted_data[10])
                    self.speed_z = float(self.splitted_data[12].split(";")[0])

                    self.battery = float(self.splitted_data[12].split(";")[2])

                    self.json_data = {
                        "lat": self.lat,
                        "lon": self.lon,
                        "altitude": self.altitude,
                        "heading": self.heading,
                        "roll": self.roll,
                        "pitch": self.pitch,
                        "yaw": self.yaw,
                        "speed_x": self.speed_x,
                        "speed_y": self.speed_y,
                        "speed_z": self.speed_z,
                        "battery": self.battery,
                    }

                    self.json_data_str = json.dumps(self.json_data)


                    self.data_publisher.publish(str(data[0]))
                    self.json_publisher.publish(self.json_data_str)                   
                with open(self.file, 'w') as f_out:
                    f_out.writelines(data[1:])

            except:
                print("Error")

            rospy.sleep(1)


com = CommPort()

if __name__ == "__main__":
    com.get_Xbee()
                