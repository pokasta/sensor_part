#!/usr/bin/env python 

import rospy
import tsys01

from std_msgs.msg import Float32

class TsysInterface(object):
    def __init__(self):
        rospy.init_node('Temperature_node')

        self.Temp_ind = rospy.Publisher(
            'instant/Temperature',
            Float32,
            queue_size=1)

        self.tsys = tsys01.TSYS01()

        if not self.tsys.init():
            rospy.logfatal('failed to initialize the sensor')
        else:
            if not self.tsys.read():
                rospy.logfatal('fatal to read Tsys01!')
            else:
                rospy.loginfo('Successfully initilised instant temp sesnsor')

        self.talker()
    def talker(self):
        while not rospy.is_shutdown():
            inst_temp = self.tsys.temperature(tsys01.UNITS_Centigrade)
            self.Temp_ind.publish(inst_temp)
        else:
            rospy.roswarn('Failed to read Temperature sensor ')
        rospy.Rate(10).sleep()
if __name__ == "__main__":
    try:
        temp_node = TsysInterface()
        rospy.spin()
    except IOError:
        rospy.logerr('IOError caught , shutting down.')
    except rospy.ROSInterruptException:
        pass