#!/usr/bin/env python3
import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer
from my_robot_interfaces.action import RobotMovement
from rclpy.action.server import ServerGoalHandle
     
     
class RobotMovementServerNode(Node):
    def __init__(self):
        super().__init__("robot_movement_server")
        self.robot_position_ = 50
        self.robot_movement_server_ = ActionServer(self,
                                                   RobotMovement,
                                                   "robot_movement",
                                                   execute_callback=self.execute_callback,
                                                    )
        self.get_logger().info("Server has been started")
        self.get_logger().info("Robot Position :" + str(self.robot_position_))
    
    def execute_callback(self,goal_handle: ServerGoalHandle):
        #Recieve the goal
        target_position = goal_handle.request.position
        velocity = goal_handle.request.velocity

        result = RobotMovement.Result()
        feedback = RobotMovement.Feedback()

        #Execute the goal
        self.get_logger().info("Executing the goal")
        while rclpy.ok():
            diff = target_position -self.robot_position_
            if diff == 0:
                result.position = self.robot_position_
                result.message = "Success"
                goal_handle.succeed()
            elif diff > 0:
                if diff >= velocity:
                    self.robot_position_ += velocity
                else:
                    self.robot_position_ += diff
            else:
                if abs(diff) >= velocity:
                   self.robot_position_ -= velocity
                else:
                    self.robot_position_ -= abs(diff)

            feedback.current_position = self.robot_position_
            goal_handle.publish_feedback(feedback)

            time.sleep(1.0)
            
        
     
def main(args=None):
    rclpy.init(args=args)
    node = RobotMovementServerNode()
    rclpy.spin(node)
    rclpy.shutdown()
     
     
if __name__ == "__main__":
    main()
