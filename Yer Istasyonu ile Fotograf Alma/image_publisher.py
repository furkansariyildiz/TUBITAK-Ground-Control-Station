#import serial
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

#RASP TARAFINDAN CALISTIRILACAK KOD

"""
def load_image( infilename ) :
    img = Image.open( infilename )
    img.load()
    data = np.asarray( img, dtype="int32" )
    return data

def save_image( npdata, outfilename ) :
    array_image = scipy.misc.imread()


data = load_image("Screenshot from 2020-12-09 18-38-55.png")

save_image(data, "selam.png")
"""

class Transform():
    def __init__(self):
        rospy.init_node("image_process_node", anonymous = True)
        self.image_path = "selam.png"
        self.image_publisher = rospy.Publisher("/comm/send_image", Image, queue_size = 10)
        self.width = 800
        self.height = 800
        self.bridge = CvBridge()


    def image_to_array(self):
        """
        array_image = scipy.misc.imread(self.image_path)
        array_resized_image = scipy.misc.imresize(array_image, (self.height, self.width), interp='nearest', mode=None)
        #print(array_resized_image)
        #self.image_publisher.publish(str(array_resized_image))
        array_resized_image = np.array(array_resized_image, dtype= int)
        self.cv_image = self.bridge.imgmsg_to_cv2(array_resized_image)
        self.image_publisher(self.cv_image)
        """
        #image = np.array(PIL.Image.open(self.image_path).convert('L'))
        image = PIL.Image.open(self.image_path)
        data = np.asarray(image)
        im = np.frombuffer(data, dtype=np.uint8).reshape(self.height, self.width, -1)
        #print(data)
        #self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        self.image_publisher.publish(self.bridge.cv2_to_imgmsg(im))


if __name__ == "__main__":
    transform = Transform()
    while True:
        transform.image_to_array()
        rospy.sleep(1)


#scipy.misc.imsave("selam.png", array_resized_image)
