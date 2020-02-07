#! /usr/bin/env python

import rospy 
from sensor_msgs.msg import Joy

rospy.init_node('joystick_node',anonymous=True)

sub = rospy.Subscriber('joy_throttle',Joy ,callback_method , queue_size=1)
pub_motion = rospy.Publisher('command',)