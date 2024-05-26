#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.action import RobotMovement
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
     
     
class RobotMovementClientNode(Node):
    def __init__(self):
        super().__init__("robot_movement_client")
        self.count_until_client_ = ActionClient(self, RobotMovement, "robot_movement")

    def send_goal(self, target_position, velocity):
        self.count_until_client_.wait_for_server()

        goal = RobotMovement.Goal()
        goal.position = target_position
        goal.velocity = velocity

        self.count_until_client_.send_goal_async(goal).add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        self.goal_handle_ : ClientGoalHandle = future.result()
        if self. goal_handle_.accepted:
            self.get_logger().info("Goal was accepted")
            self.goal_handle_.get_result_async().add_done_callback(self.goal_result_callback)
        else:
            self.get_logger().info("Goal was rejected")

    def goal_result_callback(self, future):
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Success")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().error("Aborted")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn("Canceled")
        result = future.result().result
        self.get_logger().info("Result :" + str(result.reached_number))


        
    
     
def main(args=None):
    rclpy.init(args=args)
    node = RobotMovementClientNode()
    rclpy.spin(node)
    rclpy.shutdown()
     
     
if __name__ == "__main__":
    main()
