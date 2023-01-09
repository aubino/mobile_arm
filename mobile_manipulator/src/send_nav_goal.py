#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def SendNavigationGoal() :
	rospy.loginfo('... navigation-client starting')
	client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
	client.wait_for_server()
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = "map"
	goal.target_pose.header.stamp = rospy.Time.now()

	goal.target_pose.pose.position.x = 0
	goal.target_pose.pose.position.y = 0
	goal.target_pose.pose.position.z = 0.0
	goal.target_pose.pose.orientation.x = 0.0
	goal.target_pose.pose.orientation.y = 0.0
	goal.target_pose.pose.orientation.z = 0.000899836262279
	goal.target_pose.pose.orientation.w = 0.999999595147
	client.send_goal(goal)

	wait = client.wait_for_result()
	# If the result doesn't arrive, assume the Server is not available
	if not wait:
	    rospy.logerr("Action server not available!")
	    rospy.signal_shutdown("Action server not available!")
	else:
	# Result of executing the action
	    return client.get_result()
        
if __name__ == '__main__' :
    rospy.init_node('send_navigation_goal')
    try :
        result = SendNavigationGoal()
        rospy.spin()
        if result:
            rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException as e :
        rospy.logerr('Something went wrong: %s', e)
