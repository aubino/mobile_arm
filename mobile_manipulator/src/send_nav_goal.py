#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseArray
from std_msgs.msg import Int8

def callback(box_location):
    
    # box_location = {"pos.x":0, "pos.y":0, "pos.z":0, "rot.x":0, "rot.y":0, "rot.z":0, "rot.w":0}
    # box_location["pos.x"] = data.x
    # box_location["pos.y"] = data.y
    rospy.loginfo('... navigation-client starting')
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = box_location.position.x
    goal.target_pose.pose.position.y = box_location.position.y
    goal.target_pose.pose.position.z = box_location.position.z
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.000899836262279
    goal.target_pose.pose.orientation.w = 0.999999595147
    client.wait_for_server()
    client.send_goal(goal)
    wait = client.wait_for_result()
    
    # If the result doesn't arrive, assume the Server is not available
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
    # Result of executing the action
        if client.get_result():
            rospy.loginfo("Goal execution done!")
            
            
def publisher ():
    # rospy.init_node('box_id_trigger', anonymous="True") #publish an integer in box_id_request to trigger box_identificator
    rospy.Subscriber("up_camera/box_location", PoseArray, callback)
    pub = rospy.Publisher("box_id_request",Int8, queue_size = 1)
    msg = Int8()
    msg.data = 10
    a = pub.publish(msg)
    print("Box id request sent")
    rospy.spin()
    
def SendNavigationGoal():
    # global box_location
    rospy.init_node('send_navigation_goal')
    publisher () #send a request to start processing up_camera images
    
if __name__ == '__main__' :    
    try :
        SendNavigationGoal()
    except rospy.ROSInterruptException as e :
        rospy.logerr('Something went wrong: %s', e)
