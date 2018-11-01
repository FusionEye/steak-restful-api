# -*- coding: utf-8 -*-
import time

import rosbag
import roslaunch
import rospy
from roslaunch.parent import ROSLaunchParent
from sensor_msgs.msg import PointCloud2


class RosCommon:

    def __init__(self, bag='.bag', init_node=False):
        self.init_node = init_node
        self.bag = rosbag.Bag('/data/' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + bag, 'w')

        if not self.init_node:
            rospy.init_node('listener', disable_signals=True, anonymous=True)

    def __del__(self):
        if self.init_node:
            rospy.signal_shutdown('ROS_Wait_For_Msg done')

    def process_pcd_data(self, data):
        self.bag.write('PointCloud2', data)

    def record(self, topic='/hokuyo_points'):
        rospy.Subscriber(topic, PointCloud2, self.process_pcd_data)

        rate = rospy.Rate(1)  # 10hz
        while not rospy.is_shutdown():
            rate.sleep()
        else:
            self.bag.close()

    @staticmethod
    def close():
        rospy.signal_shutdown('ros node shutdown')

    @staticmethod
    def launch_start(launch_file=''):
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        launch = roslaunch.parent.ROSLaunchParent(uuid, [launch_file])
        launch.start()
        rospy.loginfo("started")

        # 120 seconds later
        rospy.sleep(120)

        # shutdown
        launch.shutdown()

    @staticmethod
    def hokuyo_launch():
        args = ['roslaunch', 'spin_hokuyo', 'tilt_continuous.launch']
        roslaunch.main(args)

    @staticmethod
    def core_start():
        parent = ROSLaunchParent('core', [], is_core=True)
        parent.start()