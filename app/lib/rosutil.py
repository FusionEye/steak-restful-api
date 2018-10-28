# -*- coding: utf-8 -*-
import rosbag
import roslaunch
from roslaunch.parent import ROSLaunchParent
import rospy
import time
import threading
from sensor_msgs.msg import PointCloud2

bag = rosbag.Bag('/data/' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.bag', 'w')


def process_pcd_data(data):
    bag.write('PointCloud2', data)


def record(topic='/hokuyo_points'):
    thread = threading.Thread(target=lambda: rospy.init_node('record_node', disable_signals=True, anonymous=True))
    thread.start()
    rospy.Subscriber(topic, PointCloud2, process_pcd_data)

    rate = rospy.Rate(1)  # 10hz
    while not rospy.is_shutdown():
        rate.sleep()
    else:
        bag.close()


def close():
    rospy.signal_shutdown('ros node shutdown')


def launch_start(launch_file=''):
    thread = threading.Thread(target=lambda: rospy.init_node('launch_node', disable_signals=True, anonymous=True))
    thread.start()
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, [launch_file])
    launch.start()
    rospy.loginfo("started")

    # 120 seconds later
    rospy.sleep(120)

    # shutdown
    launch.shutdown()


def core_start():
    parent = ROSLaunchParent('core', [], is_core=True)
    parent.start()