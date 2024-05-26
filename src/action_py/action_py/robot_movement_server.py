#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from my_robot_interfaces.action import RobotMovement
from rclpy.action.server import ServerGoalHandle
     
     
class RobotMovementServerNode(Node):
    def __init__(self):
        super().__init__("robot_movement_server")
        self.robot_movement_server_ = ActionServer(self,
                                                   RobotMovement,
                                                   "robot_movement",
                                                   execute_callback=self.execute_callback,
                                                    )
    
    def execute_callback(self,goal_handle: ServerGoalHandle):
        #Recieve the goal
        target_position = goal_handle.request.position
        velocity = goal_handle.request.velocity

        #Execute the goal
        self.get_logger().info("Executing the goal")
        distance = 50
        for target_position in range(0,100):
            distance += velocity
     
def main(args=None):
    rclpy.init(args=args)
    node = RobotMovementServerNode()
    rclpy.spin(node)
    rclpy.shutdown()
     
     
if __name__ == "__main__":
    main()
