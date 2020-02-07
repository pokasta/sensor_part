#!/usr/bin/env python

import rospy
import ms5837


from std_msgs.msg import Float32

class Ms5837InterfaceNode(object):
    def __init__(self):
        rospy.init_node('pressure_node')

        self.pub_pressure = rospy.Publisher(
            'sensors/pressure',
            Float32,
            queue_size=1)

        self.pub_temp = rospy.Publisher(
            'sensors/temperature',
            Float32,
            queue_size=1)

        self.ms5837 = ms5837.MS5837_02BA(0)
        if not self.ms5837.init():
            rospy.logfatal('Failed to initialise MS5837! Is the sensor connected?')
        else:
            if not self.ms5837.read():
                rospy.logfatal('Failed to read MS5837!')
            else:
                rospy.loginfo('Successfully initialised MS5837')
        self.talker()

    def talker(self):
        

        while not rospy.is_shutdown():
            if self.ms5837.read():
                
                pressure_msg = self.ms5837.pressure(ms5837.UNITS_Pa)

                 
                temp_msg = self.ms5837.temperature()

                self.pub_pressure.publish(pressure_msg)
                self.pub_temp.publish(temp_msg)
            else:
                rospy.roswarn('Failed to read pressure sensor!')

            rospy.Rate(10).sleep()


if __name__ == '__main__':
    try:
        pressure_node = Ms5837InterfaceNode()
        rospy.spin()
    except IOError:
        rospy.logerr('IOError caught, shutting down.')
    except rospy.ROSInterruptException:
        pass
