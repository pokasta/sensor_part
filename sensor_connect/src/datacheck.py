#! /usr/bin/env python

import rospy 
from time import sleep
import roslib
import numpy as np
import os

try:
    import pygame
    from pygame.locals import *
    HAVE_PYGAME =True
except:
    HAVE_PYGAME = False

from std_msgs.msg import String
os.environ["SDL_VIDEODRIVER"] = "dummy"
print(HAVE_PYGAME)
pygame.init()
pygame.joystick.init()
js = pygame.joystick.Joystick(0)
print(js.get_name())
js.init()
Thrust_matrix = np.transpose(np.array([[1,1,-1,-1,0,0],[0,0,0,0,0,0],[0,0,0,0,1,1],[1,-1,1,-1,0,0]]))
rospy.init_node("Thrust",anonymous=True)
pub=rospy.Publisher('Thrust_values',String,queue_size = 10)

def listtostring(x):
    str1 =""
    str1 += "$,"
    for ele in x:
    
        str1 += str(ele)
        str1 += ","
    str1 += "#"
    str1 += "\t"
    return str1


def rescale1(val, in_min, in_max, out_min, out_max):
    i = 0
    data =[]
    for i in range(len(val[0])):
        data.append(out_min + (float(val[0][i]) - in_min)*((out_max-out_min)/(in_max - in_min)))
        i +=1
    return data   

while 1:
    pygame.event.pump()
   
    Throttle_factor = js.get_axis(2)
    Roll_factor = js.get_axis(0)
    Pitch_factor = js.get_axis(1)
    Yaw_factor = js.get_axis(3)
    #print(Throttle_factor , Roll_factor , Yaw_factor)
    Joystick_vector = np.transpose(np.array([[Throttle_factor],[Roll_factor],[Pitch_factor],[Yaw_factor]]))
    #print(Joystick_vector.shape)
    
    thruster_allocation_matrix = Thrust_matrix
    Thrust_vector = np.inner(Joystick_vector , thruster_allocation_matrix)
    #print(Thrust_vector)
    #print(list(Thrust_vector))
    data = Thrust_vector.tolist()
    values= rescale1(data,-1,1 ,1200,1800)
    new_list = [] 
    for item in values:
        new_list.append(int(item))
        
    print(new_list)
    data = listtostring(new_list)
    pub.publish(data)
    print(data ,type(data))
    sleep(0.001)
