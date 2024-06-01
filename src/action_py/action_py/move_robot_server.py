#!/usr/bin/env python3
import rclpy
import time
from rclpy.node import Node
from my_robot_interfaces.action import RobotMovement
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle, GoalResponse
     
     
class MoveRobotServer(Node):
    def __init__(self):
        super().__init__("move_robot_server")
        self.robot_position_ = 50
        self.move_robot_server_ = ActionServer(self,
                                               RobotMovement,
                                               "robot_movement",
                                               goal_callback=self.goal_callback,
                                               execute_callback=self.execute_callback)
        self.get_logger().info("action server has been started")
        self.get_logger().info("Robot Position: " + str(self.robot_position_))

    def goal_callback(self, goal_request: RobotMovement.Goal):
        self.get_logger().info("Recieved a Goal")

        if goal_request.position not in range(0, 100) or goal_request.velocity <= 0:
            self.get_logger().info("Invalid position/velocity, rejecting the goal")
            return GoalResponse.REJECT
        self.get_logger().info("accepting the goal")
        return GoalResponse.ACCEPT

    def execute_callback(self, goal_handle: ServerGoalHandle):

        #getting the goal request
        position = goal_handle.request.position
        velocity = goal_handle.request.velocity

        result =  RobotMovement.Result()
        feedback = RobotMovement.Feedback()
        
        #executing the goal
        self.get_logger().info("execute the goal")
        while rclpy.ok():
            diff = position - self.robot_position_
            if diff == 0:
                result.position = self.robot_position_
                result.message ="Success"
                goal_handle.succeed()
                return result
            elif diff > 0:
                if diff >= velocity:
                    self.robot_position_ +=velocity
                else:
                    self.robot_position_ +=diff
            else:
                if abs(diff) >=velocity:
                    self.robot_position_ -= velocity
                else:
                    self.robot_position_ -= abs(diff)

            self.get_logger().info("Robot Position: " + str(self.robot_position_))
            feedback.current_position = self.robot_position_
            goal_handle.publish_feedback(feedback)

            time.sleep(1)

            

     
def main(args=None):
    rclpy.init(args=args)
    node = MoveRobotServer()
    rclpy.spin(node)
    rclpy.shutdown()
     
     
if __name__ == "__main__":
    main()