#!/usr/bin/env python

import rospy
from sensor_connect.msg import sensor
def callback_function(message):
    rospy.loginfo("new data received :(%.2f,%.2f)",message.id,message.sensor1)





rospy.init_node('receiver',anonymous= True)
rospy.Subscriber('data',sensor,callback_function)
rospy.spin()