#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from my_robot_interfaces.msg import HardwareStatus

class NumberPublisherNode(Node):  # MODIFY NAME
    def __init__(self):
        super().__init__("number_publisher")  # MODIFY NAME
        # self.declare_parameter("test123")
        # self.declare_parameter("number_to_publish", 2)

        # self.number_ = self.get_parameter("number_to_publish").value
        self.publisher = self.create_publisher(HardwareStatus, "number", 10)
        self.timer = self.create_timer(0.5, self.publish_numbers)
        self.get_logger().info("publishing numbers")


    def publish_numbers(self):
        msg1 = HardwareStatus()
        msg1.debug_message = "chutiye"
        self.publisher.publish(msg1)

def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()  # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
