#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.action import RobotMovement
     
     
class RobotMovementClientNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("robot_movement_client") # MODIFY NAME
    
     
def main(args=None):
    rclpy.init(args=args)
    node = RobotMovementClientNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
     
     
if __name__ == "__main__":
    main()
