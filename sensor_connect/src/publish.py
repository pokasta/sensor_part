#!/usr/bin/env python


import rospy
import tsys01
from sensor_connect.msg import sensor

sensor = tsys01.TSYS01()

if not sensor.init():
    print("Error initializing pressure sensor")
    exit(1)

pub = rospy.Publisher('data',sensor,queue_size=20)

rospy.init_node('sender',anonymous=True)


rate = rospy.Rate(1)

while not rospy.is_shutdown():
    sensor_data = sensor()
    sensor_data.id = 1.0
    print(sensor.temperature())
    sensor_data.sensor = sensor.temperature()

    rospy.loginfo(" im sending")

    pub.publish(sensor_data)

    rate.sleep()
