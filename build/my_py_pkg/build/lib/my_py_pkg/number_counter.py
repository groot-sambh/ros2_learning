#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class NumberCounterNode(Node):
    def __init__(self):
        super().__init__("number_counter")

        self.subscriber = self.create_subscription(Int64, "number", self.write_numbers2, 10)
        self.counter = 0
        self.get_logger().info("number_counter subscriber created")

        self.server = self.create_service(SetBool, "reset_counter", self.callback_reset_counter)
        self.get_logger().info("reset_counter service has started")

        self.publisher = self.create_publisher(Int64, "number_count", 10)
        self.timer = self.create_timer(0.5, self.publish_numbers2)
        self.get_logger().info("Number counter has started")




    def write_numbers2(self, msg1):
        self.get_logger().info(str(msg1.data))
        self.counter = self.counter + msg1.data
        #self.counter += msg1.data

    def callback_reset_counter(self, request, response):
        if request.data == False:
            self.counter = 0
            response.success = True
            response.message = "counter has been reset"
        else:
            response.success = False
            response.message = "counter has not been reset"
        return response

        # if request.data == False:
        #     self.counter = 0
        #     self.get_logger().info("Counter reset to 0")
    def publish_numbers2(self):
        msg2 = Int64()
        msg2.data = self.counter
        self.publisher.publish(msg2)




def main(args=None):
    rclpy.init(args=args)
    node = NumberCounterNode()  # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
