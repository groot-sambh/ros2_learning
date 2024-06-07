#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup

class Node1(Node):
    def __init__(self):
        super().__init__("node1")
        self.cb_group1_ = ReentrantCallbackGroup()
        self.cb_group2_ = MutuallyExclusiveCallbackGroup()
        self.timer1_ = self.create_timer(
            1.0, self.callback_timer1, callback_group=self.cb_group2_)
        self.get_logger().info('Subscription 1 initialized')
        self.timer2_ = self.create_timer(
            1.0, self.callback_timer2, callback_group=self.cb_group1_)
        self.get_logger().info('Subscription 2 initialized')
        self.timer3_ = self.create_timer(
            1.0, self.callback_timer3, callback_group=self.cb_group1_)
        self.get_logger().info('Subscription 3 initialized')

    def callback_timer1(self):
        time.sleep(2.0)
        self.get_logger().info("cb 1")

    def callback_timer2(self):
        time.sleep(2.0)
        self.get_logger().info("cb 3")

    def callback_timer3(self):
        time.sleep(2.0)
        self.get_logger().info("cb 2")


def main(args=None):
    rclpy.init(args=args)
    node1 = Node1()
    executor = MultiThreadedExecutor()
    executor.add_node(node1)
    executor.spin()
    rclpy.shutdown()


if __name__ == "__main__":
    main()