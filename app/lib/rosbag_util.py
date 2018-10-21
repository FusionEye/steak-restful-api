# -*- coding: utf-8 -*-
import rospy
import rosbag
from sensor_msgs.msg import PointCloud2

bag = rosbag.Bag('hokuyo.bag', 'w')


def process_pcd_data(data):
    bag.write('PointCloud2', data)


def record(topic='/hokuyo_points'):
    rospy.init_node('drone_track_data')
    rospy.Subscriber(topic, PointCloud2, process_pcd_data)

    rate = rospy.Rate(1)  # 10hz
    while not rospy.is_shutdown():
        rate.sleep()
    else:
        bag.close()


def close():
    rospy.signal_shutdown()