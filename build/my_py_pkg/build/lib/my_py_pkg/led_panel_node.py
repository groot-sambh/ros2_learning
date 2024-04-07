#!/usr/bin/env python3
from urllib import response

import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLed
from my_robot_interfaces.msg import LedStateArray


class LedPanelNode(Node):
    def __init__(self):
        super().__init__("led_panel")
        self.led_states = [0, 0, 0]


        self.set_led_service = self.create_service(SetLed, "set_led", self.callback_set_led)
        self.get_logger().info("led panel node started")

        self.publisher = self.create_publisher(LedStateArray, "led_panel_state", 10)
        self.timer = self.create_timer(4.0, self.callback_led)

    def callback_set_led(self, request, response):
        if request.led_number > len(self.led_states) or request.led_number <= 0:
            response.success = False
            return response

        self.led_states[request.led_number - 1] = request.state
        response.success = True
        self.callback_led()


        # if request.led_number == 1:
        #     if request.state == True:
        #         self.led1_Signal = True
        #         response.success = True
        #     elif request.state == False:
        #         self.led1_Signal = False
        #         response.success = False
        #
        # elif request.led_number == 2:
        #     if request.state == True:
        #         self.led2_Signal = True
        #         response.success = True
        #     elif request.state == False:
        #         self.led2_Signal = False
        #         response.success = False
        #
        # elif request.led_number == 3:
        #     if request.state == True:
        #         self.led3_Signal = True
        #         response.success = True
        #     elif request.state == False:
        #         self.led3_Signal = False
        #         response.success = False
        return response

    def callback_led(self):
        msg = LedStateArray()
        msg.led_state = self.led_states
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = LedPanelNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
