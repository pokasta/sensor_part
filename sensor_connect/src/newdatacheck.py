#! /usr/bin/env python

import rospy
from time import sleep
import roslib
import numpy as np 
import os


try:
    import pygame
    from pygame.locals import *
    HAVE_PYGAME = True
except:
    HAVE_PYGAME = False

from std_msgs.msg import String
os.environ["SDL_VIDEODRIVER"] = "dummy"

print(HAVE_PYGAME)
pygame.init()
js = pygame.joystick.Joystick(0)
print(js.get_name())
js.init()
pub = rospy.Publisher('Angle_values',String , queue_size= 10)
rospy.init_node('Angle',anonymous= True)

def listtostring(x):
    str1 = ""
    str1 += "$"
    str1 += ","
    for ele in x:
        str1 += str(ele)
        str1 += ","
    str1 += "#"
    str1 += "\t"
    return str1


def rescale(val ,in_min , in_max , out_min , out_max):
    i = 0
    data = []
    for i in range(len(val[0])):
        data.append(out_min + (float(val[0][i])-in_min)*((out_max-out_min)/(in_max - in_min)))
        i += 1
    return data

while 1:
    pygame.event.pump()
    Angle_factor = js.get_axis(0)
    Tilt_vector = js.get_axis(1)

    camera_vector = np.transpose(np.array([[Angle_factor],[Tilt_vector]]))

    data = camera_vector.tolist()
    values = rescale(data , -1 ,1 , 900 , 2100)
    new_list = []
    for item in values:
        new_list.append(int(item))
    #print(new_list)
    data = listtostring(new_list)
    print(data)
    pub.publish(data)
    sleep(.001)

    