cmake_minimum_required(VERSION 2.8.3)
project(sensor_connect)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  sensor_msgs
  actionlib_msgs
  message_generation
  cv_bridge
  image_transport
)




## Generate added messages and services with any dependencies listed here
 generate_messages(
   DEPENDENCIES
   std_msgs
   sensor_msgs
)



catkin_package(
  INCLUDE_DIRS 
  CATKIN_DEPENDS roscpp rospy std_msgs message_runtime sensor_msgs
  
)

catkin_package(CATKIN_DEPENDS message_runtime std_msgs)

