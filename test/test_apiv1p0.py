# -*- coding: utf-8 -*-
import unittest

from app.lib import fileutil


class TestApiv1p0(unittest.TestCase):
    def test_get_ros_bag_files(self):
        result = fileutil.get_ros_bag_files(
            "/Users/Leon/Documents/git/beibq/test")
        print(result)


if __name__ == '__main__':
    unittest.main()
