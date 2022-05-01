import rospy
from std_msgs.msg import String
#from encoder import Encoder
import threading
import time
#import port_finder
import PIL.Image
import scipy.misc
import numpy as np
from cv_bridge import CvBridge
from io import BytesIO
from sensor_msgs.msg import Image
import base64
import cv2
import os


#YER ISTASYONU TARAFINDAN CALISTIRILACAK KOD
"""
Yer istasyonuna gelecek olan fotograflari -ki bunlar np array olarak iletilmeli- arayuzde gosterilmesini saglamaktadir.
"""

class Image_Subscriber():
    def __init__(self):
        rospy.init_node("image_transform_node", anonymous = True)
        self.new_image = "deneme.png"
        self.npdata = []
        self.bridge = CvBridge()
        self.cv_image = None
        rospy.Subscriber("/mybot/camera1/image_raw", Image, self.image_callBack)


        



    def image_callBack(self, msg):
        self.cv_image = self.bridge.imgmsg_to_cv2(msg)
        #print(self.cv_image)
        (rows,cols,channels) = self.cv_image.shape
        if cols > 60 and rows > 60 :
            cv2.circle(self.cv_image, (50,50), 10, 255)

        
        cv2.imshow("Image Window", self.cv_image)
        cv2.waitKey(3)

    def array_to_image(self):
        if self.npdata != []:
            pass
            
           

if __name__ == "__main__":
    image_sub = Image_Subscriber()
    sayac = 0
    path_for_delete_images = "../ground_control_station/team_imu/static/images/"

    try:
        for files in os.listdir(path_for_delete_images):
            os.remove(os.path.join(path_for_delete_images, files))
    except:
        print("Hata")

    while True:
        path = "../ground_control_station/team_imu/static/images/" + str(sayac) + ".png" 
        
        image_sub.array_to_image()
	if image_sub.cv_image != [] and not path.endswith("0.png"):	
        	cv2.imwrite( path,image_sub.cv_image)
        sayac = sayac + 1
        print(path)
        rospy.sleep(0.5)
