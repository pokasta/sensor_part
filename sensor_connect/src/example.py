#! /usr/bin/env python3

import tsys01
import ms5837
from time import sleep
from std_msgs.msg import Float32

from brping import Ping1D
import rospy
from sensor_msgs.msg import FluidPressure , Temperature

sensor3 = Ping1D("/dev/ttyUSB0",115200)


sensor_data = tsys01.TSYS01()
pressure_data = ms5837.MS5837_02BA(0)

if not sensor_data.init():
    print("Error initializing sensor")
    rospy.logfatal('failed to initialise MS5873 ! Is the sensor connected ?')
    exit(1)
if not pressure_data.init():
    print("Sensor could not be initialized")
    exit(1)


instant_temperature = rospy.Publisher('Instant/Temperature',Temperature,queue_size=1)
pub1 = rospy.Publisher('Altimeter',Float32,queue_size=1)
pub_pressure = rospy.Publisher('sensors/Pressure',FluidPressure,queue_size=20)
pub_temp = rospy.Publisher('sensors/Temperature',Temperature,queue_size=20)
rospy.init_node('Pressure_node',anonymous=True)


pressure_message = FluidPressure()
pressure_message.variance = 0
temp_message = Temperature()
temp_message.variance = 0
instant_temp = Temperature()
instant_temp.variance = 0

rate = rospy.Rate(1)
while True:
    if not sensor_data.read():
        print("Error reading sensor")

        exit(1)
    instant_temp.header.stamp = rospy.get_rostime()
    instant_temp.temperature = sensor_data.temperature()
    instant_temperature.publish(instant_temp)

    if pressure_data.read():

        pressure_message.header.stamp = rospy.get_rostime()
        pressure_message.fluid_pressure = pressure_data.pressure(ms5837.UNITS_atm)
        temp_message.header.stamp = rospy.get_rostime()
        temp_message.temperature = pressure_data.temperature()
        pub_pressure.publish(pressure_message)
        pub_temp.publish(temp_message)
    else:
        print("Sensor read failed!")
        rospy.roswarn("Failed to read pressure sensor !")
        exit(1)
    data = sensor3.get_distance_simple()

    if data:
        print("Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
        sensor = data.get("distance")
        pub1.publish(sensor)
    else:
        print("Failed to get distance data")
    rospy.Rate(10).sleep()

    #pub2.publish(pressure_data_send)
    #pub3.publish(data1)
    
    sleep(.1)