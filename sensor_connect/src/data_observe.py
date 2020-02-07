#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
import serial
global buttons_map
global axes_map
global ser
global pub 
global flag1
import numpy as np
from time import sleep
from std_msgs.msg import String
from sensor_msgs.msg import Temperature
flag2 =0
#ser = serial.Serial("/dev/ttyACM0", 9600)

def on_off(light):
    flag1 = 0
    if light % 2 == 0:
        flag1 =100

    else :
        flag1 =200
    return flag1

def rescale(val , in_min , in_max , out_min , out_max):
    i = 0 
    data = []
    for i in range(len(val[0])):
        data.append(out_min + (float(val[0][i])- in_min) *((out_max-out_min)/(in_max-in_min)))
        i += 1
    return data 

def listtostring(x):
    str1 = ""
    str1 += "$,"
    for ele in x:
        str1 += str(ele)
        str1 += ","
    #str1 += "#"
    #str1 += "\t"
    return str1
def callback2(msg):
    print(msg.data)

def callback(msg):
    global flag2
    buttons_map = ['A','B','X','Y','LB','RB','back','start','power','stick_button_left','stick_button_right','extra']
    axes_map = ['horizontal','verticle','upward','extra','manipulator','extra1','extra2']

    buttons = {}
    axes = {}
    print("working ?")
    
    for i in range(len(msg.buttons)):
        buttons[buttons_map[i]] = msg.buttons[i]
    for j in range(len(msg.axes)):
        axes[axes_map[j]] = msg.axes[j]
    

    hor = axes['horizontal']
    ver = axes['verticle']
    upw = axes['upward']

    yaw = axes['extra']
    mani= axes['manipulator'] 

    light = buttons['A']
    print(light)
    flag2 = flag2 + light
    print(flag2)
    
    data_flag = on_off(light)
    
    print(data_flag)
    

    print(hor,ver , upw ,yaw, mani)


    Thrust_matrix = np.transpose(np.array([[1,1,-1,-1,0,0],[0,0,0,0,0,0],[0,0,0,0,1,1],[1,-1,1,-1,0,0]]))

    joystic_vector = np.transpose(np.array([[ver],[hor],[upw],[yaw]]))

    thrust_vector = np.inner(joystic_vector,Thrust_matrix)

    data = thrust_vector.tolist()
    values = rescale(data,-1,1,1400,1600)
    new_list = []
    for item in values:
        new_list.append(int(item))
    data_string = listtostring(new_list)
    if flag2 % 2 == 0:
        data_string += "1100,#"
        data_string += "\t"

    else:
        data_string += "1900,#"
        data_string += "\t"
    print(data_string)

    print(bytearray(data_string ,encoding='utf-8'))
    #ser.write(bytearray(data_string ,encoding='utf-8'))
    
    
    
    sleep(1)


def datawer():
    rospy.init_node('joystick_node')
    sub = rospy.Subscriber('joy_throttle',Joy ,callback,queue_size=1)
    

    

    
if __name__ == "__main__":
    global flag2 
    datawer()
    rospy.spin()
    


        