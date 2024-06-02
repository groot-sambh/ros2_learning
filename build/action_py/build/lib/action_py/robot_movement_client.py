#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.action import RobotMovement
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
     
     
class RobotMovementClientNode(Node):
    def __init__(self):
        super().__init__("robot_movement_client")
        self.goal_handle_ = None
        self.robot_movement_client_ = ActionClient(self, RobotMovement, "robot_movement")

    def send_goal(self, target_position, velocity):
        self.robot_movement_client_.wait_for_server()

        goal = RobotMovement.Goal()
        goal.position = target_position
        goal.velocity = velocity

        self.robot_movement_client_.send_goal_async(goal, feedback_callback=self.goal_feedback_callback)\
                                    .add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        self.goal_handle_ : ClientGoalHandle = future.result()
        if self. goal_handle_.accepted:
            self.get_logger().info("Goal was accepted")
            self.goal_handle_.get_result_async().add_done_callback(self.goal_result_callback)
        else:
            self.get_logger().info("Goal was rejected")

    def goal_result_callback(self, future):
        status = future.result().status
        result = future.result().result
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Success")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().error("Aborted")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn("Canceled")
        self.get_logger().info(str(result))
        self.get_logger().info("Result :" + str(result.reached_position))
        self.get_logger().info("Result :" + str(result.message))

    def goal_feedback_callback(self, feedback_msg):
        position = feedback_msg.feedback.current_position
        self.get_logger().info("Feedback position: " + str(position))

def main(args=None):
    rclpy.init(args=args)
    node = RobotMovementClientNode()
    node.send_goal(76, 7)
    rclpy.spin(node)
    rclpy.shutdown()
     
     
if __name__ == "__main__":
    main()
