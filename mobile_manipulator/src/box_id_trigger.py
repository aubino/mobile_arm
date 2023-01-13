#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 15:35:00 2023

@author: choroumous
"""

#!/usr/bin/env python

import rospy
from std_msgs.msg import Int8

def publisher ():
    rospy.init_node('box_id_trigger', anonymous="True") #publish an integer in box_id_request to trigger box_identificator
    pub = rospy.Publisher("box_id_request",Int8)
    msg = Int8()
    msg.data = 0
    rospy.loginfo(msg)
    pub.publish(msg)
    
if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
