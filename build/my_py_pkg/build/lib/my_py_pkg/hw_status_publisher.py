#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import HardwareStatus


class HardwareStatusPublisherNode(Node):
    def __init__(self):
        super().__init__("hardware_status_publisher")
        self.hw_status_publisher = self.create_publisher(HardwareStatus, "hw_status", 10)
        self.timer = self.create_timer(1.0, self.publish_hardware_status)
        self.get_logger().info("Hardware status publisher has been started")


    def publish_hardware_status(self):
        msg = HardwareStatus()
        msg.temperature = 45
        msg.are_motors_ready = True
        msg.debug_message = "beep-boop"
        self.hw_status_publisher.publish(msg)



def main(args=None):
    rclpy.init(args=args)
    node = HardwareStatusPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
