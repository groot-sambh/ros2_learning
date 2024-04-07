#!/usr/bin/env python3
from functools import partial
from urllib import request

import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLed

class BatteryNode(Node):  # MODIFY NAME
    def __init__(self):
        super().__init__("battery_node")  # MODIFY NAME

        self.charging_timer = self.create_timer(6, self.charging)
        self.discharging_timer = self.create_timer(4, self.discharging)

    def batery_callback(self, led_number, state):
        client = self.create_client(SetLed, "set_led")
        while not client.wait_for_service():
            self.get_logger().warm("Waiting for Server Add Two Ints...")


        request = SetLed.Request()
        request.led_number = led_number
        request.state = state

        future = client.call_async(request)
        future.add_done_callback(partial(self.writer))

    def writer(self, future):
        try:
            response = future.result()
            self.get_logger().info(str(response.success))
        except Exception as e:
            self.get_logger().error("service call failed %r" % (e, ))


    def charging(self):
        self.batery_callback(3, True)
        self.get_logger().info("charging")

    def discharging(self):
        self.batery_callback(3, False)
        self.get_logger().info("discharging")

def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()  # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
