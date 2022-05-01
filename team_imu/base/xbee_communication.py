from digi.xbee.devices import RemoteXBeeDevice, XBeeDevice, XBee64BitAddress
import rospy
from std_msgs.msg import String

class XBEE_COM:
    def __init__(self, port_, baudrate_):
        rospy.init_node("xbee_node", anonymous=False)

        self.xbee_publisher = rospy.Publisher("/data_from_vehicle", String, queue_size=10)

        rospy.Subscriber("/data_from_station", String, self.stationCallback)
        
        self.prepareXbee(port=port_, baudrate=baudrate_)


    def stationCallback(self, msg):
        self.sendData(msg.data)

    def prepareXbee(self, port, baudrate):
        xbee_is_ok = False
        while not xbee_is_ok:
            try:
                self.xbee = XBeeDevice(port, baudrate)
                self.xbee.open()
                self.remote = RemoteXBeeDevice(self.xbee, XBee64BitAddress.from_hex_string("0013A20040XXXXXX"))
                xbee_is_ok = True
            except Exception as e:
                rospy.logerr(e)



    def sendData(self, message):
        self.xbee.send_data(self.remote, message)

    def readData(self):
        rospy.loginfo("Readed data from XBEE: " + str(self.xbee.read_data()))
        self.xbee_publisher.publish(str(self.xbee.read_data()))

if __name__ == '__main__':
    xbee = XBEE_COM("COM1", 9600)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        try:
            xbee.readData()
        except Exception as e:
            rospy.logerr(e)
        rate.sleep()