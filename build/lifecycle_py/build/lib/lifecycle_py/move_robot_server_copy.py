#!/usr/bin/env python3
import rclpy
import time
import threading
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle, GoalResponse, CancelResponse
from my_robot_interfaces.action import MoveRobot
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle.node import LifecycleState, TransitionCallbackReturn

class MoveRobotServerNode(LifecycleNode):
    def __init__(self):
        super().__init__("move_robot_server_copy")
        self.activate = False
        self.goal_lock_ = threading.Lock()
        self.goal_handle_: ServerGoalHandle = None
        self.robot_position_ = 50
        self.move_robot_server_ = None
        # self.declare_parameter("action_server_name", rclpy.Parameter.Type.STRING)
        # self.server_name =self.get_parameter("action_server_name").value
        self.get_logger().info("lifecycle action server has been started")
        
    #the part of the lifecycle node
    def on_configure(self, previous_state: LifecycleState):
        self.get_logger().info("In On_Configure")
        self.move_robot_server_ = ActionServer(
            self,
            MoveRobot,
            self.server_name,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup()) 
        self.get_logger().info("Action server has been started")
        self.get_logger().info("Robot position: " + str(self.robot_position_))   
        return TransitionCallbackReturn.SUCCESS
    
    def on_cleanup(self, previous_state: LifecycleState):
        self.get_logger().info("In On_cleanup")
        self.move_robot_server_.destroy()
        return TransitionCallbackReturn.SUCCESS
    
    def on_activate(self, previous_state: LifecycleState):
        self.get_logger().info("In On_activate")
        self.activate = True

    def on_deactivate(self, state: LifecycleState):
        self.get_logger().info("In On_deactivate")
        with self.goal_lock_:
                if self.goal_handle_ is not None and self.goal_handle_.is_active:
                    self.goal_handle_.abort()
        self.activate = False

    def on_shutdown(self, state: LifecycleState):
        self.get_logger().info("In On_shutdown")
        self.move_robot_server_.destroy()
        return TransitionCallbackReturn.SUCCESS


    #the part of the action server callbacks
    def goal_callback(self, goal_request: MoveRobot.Goal):
        self.get_logger().info("Received a new goal")
        if self.activate:
            if goal_request.position not in range(0, 100) or goal_request.velocity <= 0:
                self.get_logger().warn("Invalid position/velocity, reject goal")
                return GoalResponse.REJECT
            
            # New goal is valid, abort previous goal and accept new goal
            with self.goal_lock_:
                if self.goal_handle_ is not None and self.goal_handle_.is_active:
                    self.goal_handle_.abort()
            
            self.get_logger().info("Accept goal")
            return GoalResponse.ACCEPT
        else:
            self.get_logger().info("node not activated")
            return GoalResponse.REJECT
    
    def cancel_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info("Received a cancel request")
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle: ServerGoalHandle):
        with self.goal_lock_:
            self.goal_handle_ = goal_handle

        goal_position = goal_handle.request.position
        velocity = goal_handle.request.velocity

        result = MoveRobot.Result()
        feedback = MoveRobot.Feedback()

        self.get_logger().info("Execute goal")
        while rclpy.ok():
            if not goal_handle.is_active:
                result.position = self.robot_position_
                result.message = "Preempted by another goal"
                return result
            
            if goal_handle.is_cancel_requested:
                result.position = self.robot_position_
                if goal_position == self.robot_position_:
                    result.message = "Success after cancel request"
                    goal_handle.succeed()
                else:
                    result.message = "Canceled"
                    goal_handle.canceled()
                return result

            diff = goal_position - self.robot_position_

            if diff == 0:
                result.position = self.robot_position_
                result.message = "Success"
                goal_handle.succeed()
                return result
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

            self.get_logger().info("Robot position: " + str(self.robot_position_))
            feedback.current_position = self.robot_position_
            goal_handle.publish_feedback(feedback)

            time.sleep(1.0)

    

def main(args=None):
    rclpy.init(args=args)
    node = MoveRobotServerNode()
    rclpy.spin(node, MultiThreadedExecutor())
    rclpy.shutdown()


if __name__ == "__main__":
    main()