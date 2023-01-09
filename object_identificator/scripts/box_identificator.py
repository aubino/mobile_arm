#!/usr/bin/env python3
import rospy, tf ,cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError 
from std_msgs.msg import Header
from sensor_msgs.msg import CompressedImage,Image,CameraInfo
from geometry_msgs.msg import PoseArray, Pose,Point, Quaternion
from std_msgs.msg import Int32
#from IdentifyBox.srv import IdentifyBox, IdentifyBoxResponse
import numpy as np
# the node containing this class has to have the fillowing rosparams loaded 
# -color_min : vector type containing the minimum values of the image field
# -color_max :  vector type containing the maximum value of the image field
# - camera_z :  the altitude of the camera. Used to recompute boxe 3d coordinates
# - box_z :  the heigh of the box to accurateley reconstrunct the 3d coordinates. Assuming boxz is always smaller than camera_z and of course positive
class box_identificator : 
    def __init__(self,img_topic:str,cam_info_topic:str,request_topic:str):
        self.rgb= np.zeros((480,640,3))
        self.br=CvBridge()
        self.img_topic_sub = rospy.Subscriber(img_topic,Image,self.image_callback)
        self.cam_info_topic_sub = rospy.Subscriber(cam_info_topic,CameraInfo,self.cam_info_callback)
        self.box_id_sub = rospy.Subscriber(request_topic,Int32,self.box_identification_topic_routine)
        self.box_id_pub = rospy.Publisher(rospy.get_namespace()+"/box_location",PoseArray,queue_size=1)
        self.cam_info = CameraInfo()
        #self.identification_service = rospy.Service(rospy.get_namespace()+"identify_box",IdentifyBox,self.box_identification_routine)
    
    def image_callback(self, data):
        self.rgb=self.br.imgmsg_to_cv2(data,"bgr8")

    def cam_info_callback(self, data) :
        self.cam_info = data
    
    def box_identification_routine(self,req) :
        boxes_poses = PoseArray()
        color_min = rospy.get_param(rospy.get_namespace() + "/color_min")
        color_max = rospy.get_param(rospy.get_namespace() + "/color_max")
        camera_z = rospy.get_param(rospy.get_namespace() + "/camera_z")
        box_z = rospy.get_param(rospy.get_namespace() + "/box_z")
        lower_bound = np.array([color_min[0],color_min[1],color_min[2]])
        upper_bound = np.array([color_max[0],color_max[1],color_max[2]])
        mask = cv2.inRange(self.rgb,lower_bound,upper_bound)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        squares = []
        square_center = []
        square_center3d = []
        for cnt in contours : 
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)  # approximate the contour with a polygon
            if len(approx) == 4:
                squares.append(cnt)
                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                square_center.append((cX,cY))
                #to recover the 3d coordinates, we assume that there is no distorsion 
                X = (cX - self.cam_info.K[2])*(camera_z-box_z)/self.cam_info.K[0]
                Y = (cY - self.cam_info.K[5])*(camera_z-box_z)/self.cam_info.K[4]
                square_center3d.append((X,Y,camera_z))
        
        for i in range(0,min(req.max_box,len(square_center3d))) : 
            box_pose = Pose(Point(square_center3d[i][0],square_center3d[i][1],square_center3d[i][2]),Quaternion())
            boxes_poses.poses.append(box_pose)
        boxes_poses.header.frame_id = self.cam_info.header.frame_id
        boxes_poses.header.stamp = rospy.Time.now()
        #return IdentifyBoxResponse(boxes_poses)
        return boxes_poses
    def box_identification_topic_routine(self,data) : 
        boxes_poses = PoseArray()
        color_min = rospy.get_param(rospy.get_namespace() + "/color_min")
        color_max = rospy.get_param(rospy.get_namespace() + "/color_max")
        camera_z = rospy.get_param(rospy.get_namespace() + "/camera_z")
        box_z = rospy.get_param(rospy.get_namespace() + "/box_z")
        lower_bound = np.array([color_min[0],color_min[1],color_min[2]])
        upper_bound = np.array([color_max[0],color_max[1],color_max[2]])
        mask = cv2.inRange(self.rgb,lower_bound,upper_bound)
        #cv2.imshow("Mask_of_image",mask)
        #cv2.waitKey(10)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #rospy.loginfo("Number of contours found : %s",len(contours))
        squares = []
        square_center = []
        square_center3d = []
        for cnt in contours : 
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True) # approximate the contour with a polygon
            if len(approx) == 4:
                squares.append(cnt)
                M = cv2.moments(cnt)
                try : 
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    square_center.append((cX,cY))
                    #to recover the 3d coordinates, we assume that there is no distorsion 
                    X = (cX - self.cam_info.K[2])*(camera_z-box_z)/self.cam_info.K[0]
                    Y = (cY - self.cam_info.K[5])*(camera_z-box_z)/self.cam_info.K[4]
                    square_center3d.append((X,Y,camera_z))
                except ZeroDivisionError :
                    rospy.logwarn("Contour not closed")
        for i in range(0,min(data.data,len(square_center3d))) : 
            box_pose = Pose(Point(square_center3d[i][0],square_center3d[i][1],square_center3d[i][2]),Quaternion())
            boxes_poses.poses.append(box_pose)
        boxes_poses.header.frame_id = self.cam_info.header.frame_id
        boxes_poses.header.stamp = rospy.Time.now()
        self.box_id_pub.publish(boxes_poses)
        #rospy.loginfo("Number of boxes found : %s",len(square_center))

if __name__ == "__main__":
    rospy.init_node("box_identificator_node")
    cube_finder = box_identificator("up_camera","up_camera_info","/box_id_request") 
    rospy.spin()


            


        