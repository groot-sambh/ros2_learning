#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from my_robot_interfaces.action import RobotMovement
from rclpy.action.client import ClientGoalHandle, GoalStatus
     
     
class MoveRobotClientNode(Node):
    def __init__(self):
        super().__init__("move_robot_client")
        self.move_robot_client_ = ActionClient(self,
                                               RobotMovement,
                                               "robot_movement")
        
    def send_goal(self, position, velocity):
        self.move_robot_client_.wait_for_server()

        goal = RobotMovement.Goal()
        goal.position = position
        goal.velocity = velocity
        
        self.get_logger().info("position: " + str(position) + "velocity: " + str(velocity))
        self.move_robot_client_. \
            send_goal_async(goal, feedback_callback=self.goal_feedback_callback). \
            add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle: ClientGoalHandle = future.result()
        if goal_handle.accepted:
            self.get_logger().info("goal got accepted")
            goal_handle.get_result_async().add_done_callback(self.goal_result_callback)

        else:
            self.get_logger().info("Goal got rejected")

    def goal_result_callback(self, future):
        status = future.result().status
        result = future.result().result

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Success")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().error("Aborted")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn("Canceled")

        self.get_logger().info("position: " + str(result.position))
        self.get_logger().info("message: " + str(result.message))

    def goal_feedback_callback(self, feedback_msg):
        position = feedback_msg.feedback.current_position
        self.get_logger().info("position: " + str(position))
     
     
def main(args=None):
    rclpy.init(args=args)
    node = MoveRobotClientNode()
    node.send_goal(76, 7)
    rclpy.spin(node)
    rclpy.shutdown()
     
     
if __name__ == "__main__":
    main()