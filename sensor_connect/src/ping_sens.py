#!/usr/bin/env python3

import rospy

from brping import Ping1D
from std_msgs.msg import Float32
import serial

class pingConnect(object):
    def __init__(self):
        rospy.init_node('depth_node')
        self.depth_sen = rospy.Publisher(
            'Altimeter',
            Float32,
            queue_size=1
        )

        self.ser = Ping1D("/dev/ttyUSB0" , 115200)
        self.talker()
    def talker(self):
        while not rospy.is_shutdown():
            data = self.ser.get_distance_simple()
            if data:
                print("Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
                depth_value = data.get("distance")
                self.depth_sen.publish(depth_value)
            else:
                rospy.roswarn('failed to read pressure altimeter depth data')
            rospy.Rate(10).sleep()

if __name__ == "__main__":
    try:
        Depth_node = pingConnect()
        rospy.spin()
    except IOError:
        rospy.logerr('IOError caught ,shutting dowm')
    except rospy.ROSInterruptException:
        pass
            