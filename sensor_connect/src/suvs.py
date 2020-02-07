import rospy
import serial
from std_msgs.msg import String
try:
    import pygame
    from pygame.locals import *
    HAVE_PYGAME =True
except:
    HAVE_PYGAME = False
def callback_Method(msgsdata):
    print(msgsdata.data)


def listener():
    rospy.init_node('joydata',anonymous= True)
    rospy.Subscriber("Thrust_values" ,String ,callback_Method)
    rospy.spin()

if __name__ == "__main__":
    listener()