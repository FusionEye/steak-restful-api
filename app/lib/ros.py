# -*- coding: utf-8 -*-
import time
import roslaunch
import rospy
from roslaunch.parent import ROSLaunchParent
from sensor_msgs.msg import PointCloud2
from pypcd import PointCloud


class RosCommon:

    def __init__(self, init_node=False):
        self.init_node = init_node
        if not self.init_node:
            rospy.init_node('listener', disable_signals=True, anonymous=True)
            self.pub = rospy.Publisher('out_cloud', PointCloud2, queue_size=1)

    def __del__(self):
        if self.init_node:
            rospy.signal_shutdown('ROS_Wait_For_Msg done')

    def process_pcd_data(self, msg):
        pc = PointCloud.from_msg(msg)
        pcd_file = '/data/' + time.strftime("%Y%m%d%H%M", time.localtime()) + '.pcd'
        if len(pc.pc_data) > 1000:
            pc.save(pcd_file, compression='ascii')
        # outmsg = pc.to_msg()
        # self.pub.publish(outmsg)

    def record(self, topic='/hokuyo_points'):
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
