# -*- coding: utf-8 -*-
import time
import roslaunch
import rospy
import pypcd
import logging
import numpy as np
from roslaunch.parent import ROSLaunchParent
from sensor_msgs.msg import PointCloud2
from pypcd import PointCloud


log = logging.getLogger(__name__)


class RosCommon:

    def __init__(self, init_node=False):
        self.init_node = init_node
        if not self.init_node:
            rospy.init_node('listener', disable_signals=True, anonymous=True)

    @staticmethod
    def process_pcd_data(msg):
        message_cloud = PointCloud.from_msg(msg)
        pcd_path = '/data/' + time.strftime("%Y%m%d%H%M", time.localtime()) + '.pcd'

        try:
            parent_cloud = pypcd.point_cloud_from_path(pcd_path)
        except Exception, ex:
            import traceback
            traceback.print_exc()
            log.error(ex.message)
            message_cloud.save(pcd_path)
            return

        if len(parent_cloud.pc_data) > 0:
            log.info('Concatenate two point clouds into bigger point cloud')
            # bigger cloud = a + b
            parent_cloud = pypcd.cat_point_clouds(parent_cloud, message_cloud)
            parent_cloud.save(pcd_path)

    def record(self, topic='/assembled_cloud'):
        rospy.Subscriber(topic, PointCloud2, self.process_pcd_data)
        # self.pub = rospy.Publisher('out_cloud', PointCloud2, self.process_pcd_data)
        rate = rospy.Rate(1)  # 10hz
        while not rospy.is_shutdown():
            rate.sleep()

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
        package = 'spin_hokuyo'
        launch_file = 'tilt_continuous.launch'
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        launch_file = os.path.join(rospkg.RosPack().get_path(package), 'launch', launch_file)
        launch = roslaunch.parent.ROSLaunchParent(uuid, [launch_file])
        launch.start()

    @staticmethod
    def core_start():
        parent = ROSLaunchParent('core', [], is_core=True)
        parent.start()
