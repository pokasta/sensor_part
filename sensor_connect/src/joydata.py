import pygame
import pygame.mixer
from pygame.locals import *
import numpy as np 
import rospy
from std_msgs.msg import Int32MultiArray


from time import sleep

pygame.joystick.quit()
pygame.joystick.init()


pygame.init()
#software and other kinds of works.



if pygame.joystick.get_count() == 0:
    print("plaese reconnect joystick")
    pygame.joystick.quit()
    
def rescale(val, in_min, in_max, out_min, out_max):
    i = 0
    data =[]
    #print(val[0][4])
    #print(type(val))
    
    #print(len(val))
    while i < len(val[0]):
        #print(i)
        data.append(out_min + (float(val[0][i]) - in_min)*((out_max-out_min)/(in_max - in_min)))
        i +=1
    return data   
def rescale1(val, in_min, in_max, out_min, out_max):
    i = 0
    data =[]
    for i in range(len(val[0])):
        data.append(out_min + (float(val[0][i]) - in_min)*((out_max-out_min)/(in_max - in_min)))
        i +=1
    return data   

def rescale2(val, in_min, in_max, out_min, out_max):
    i = 0
    data =[]
    for i in range(len(val[0])):
        data.append(out_min + (float(val[0][i]) - in_min)*((out_max-out_min)/(in_max - in_min)))
        i +=1
    return data
    

js = pygame.joystick.Joystick(0)
js_name = pygame.joystick.Joystick(0).get_name()
js.init()
print("i got the joystick")
print(js_name)
Thrust_matrix = np.transpose(np.array([[1,1,-1,-1,0,0],[0,0,0,0,0,0],[0,0,0,0,1,1],[1,-1,1,-1,0,0]]))
print(Thrust_matrix.shape)
pub=rospy.Publisher('Thrust_values',Int32MultiArray,queue_size = 10)

while 1:
    pygame.event.pump()
    Throttle_factor = js.get_axis(2)
    Roll_factor = js.get_axis(0)
    Pitch_factor = js.get_axis(1)
    Yaw_factor = js.get_axis(3)
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
    pub.publish(new_list)

    sleep(0.001)








