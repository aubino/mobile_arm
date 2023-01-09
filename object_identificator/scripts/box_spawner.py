#!/usr/bin/env python3

import random, rospy, tf 
from gazebo_msgs.srv import  SpawnModel
from geometry_msgs.msg import *
import argparse

def parse_cmdline():
    parser = argparse.ArgumentParser(description='Random spawner argument parser.')
    parser.add_argument('-n', '--number-of-models', type=int, nargs=None, required=True,
                        help='Set the number of models you want to spawn. Maximum is 10')
    parser.add_argument('-xm', '--x-max', type=int, nargs=None, required=True,
                        help='Maximum aeria to spawn in from x coordinates.')
    parser.add_argument('-ym', '--y-max', type=int, nargs=None, required=True,
                        help='Maximum aeria to spawn in from x coordinates.')
    parser.add_argument('-m', '--model-path', type=str, nargs=None, required=True,
                        help='Set model to spawn path.')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_cmdline()
    rospy.init_node("spawn_products_in_bins")
    print("Waiting for gazebo services...")
    rospy.wait_for_service("gazebo/spawn_sdf_model")
    spawn_model = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)
    with open(args.model_path, "r") as f:
        model_xml = f.read()
    orient = Quaternion() 
    for i in range(0,args.number_of_models) : 
        x = random.uniform(-args.x_max/2,args.x_max/2)
        y = random.uniform(-args.y_max/2, args.y_max/2)
        z = 0
        item_pose   =   Pose(Point(x,y,z),   orient)
        item_name = "box{0}".format(i)
        spawn_model(item_name, model_xml, "", item_pose, "world")
        print("Spawned the sdf in coordinate : x = ", x ," y = " ,y, " z = 0 ") 
    

