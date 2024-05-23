#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from my_robot_interfaces.action import RobotMovement,
     
     
class RobotMovementServerNode(Node):
    def __init__(self):
        super().__init__("robot_movement_server")
        self.robot_movement_server_ = ActionServer(self,
                                                   RobotMovement,
                                                   )
    
     
def main(args=None):
    rclpy.init(args=args)
    node = RobotMovementServerNode()
    rclpy.spin(node)
    rclpy.shutdown()
     
     
if __name__ == "__main__":
    main()
