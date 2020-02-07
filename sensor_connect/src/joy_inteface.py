#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy

class JoystickInterface(object):
    def __init__(self):
        rospy.init_node('joystick_node')
        self.sub = rospy.Subscriber(
            'joy_throttle',Joy,self.callback , queue_size=1
        )

        self.buttons_map = ['A', 'B', 'X', 'Y', 'LB', 'RB', 'back',
                            'start', 'power', 'stick_button_left',
                            'stick_button_right','extra']

        
        self.axes_map = ['horizontal_axis_left_stick',
                         'vertical_axis_left_stick', 'LT',
                         'horizontal_axis_right_stick',
                         'vertical_axis_right_stick', 'RT',
                         'dpad_horizontal']

    def callback(self , msg):
        buttons = {}
        axes = {}

        for i in range(len(msg.buttons)):
            buttons[self.buttons_map[i]] = msg.buttons[i]

        for j in range(len(msg.axes)):
            axes[self.axes_map[j]] = msg.axes[j]

if __name__ == "__main__":
    try:
        joystick_node = JoystickInterface()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass