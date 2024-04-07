#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

     
     
class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__("turtle_controller")
        self.pose_ = None
        self.target_x = 8.0
        self.target_y = 4.0
        self.pose_subscriber = self.create_subscription(Pose, "turtle1/pose", self.pose_subscriber_callback, 10)

        self.vel_publisher = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.timer = self.create_timer(1.0, self.vel_publisher_callback)

    def pose_subscriber_callback(self, msg):
        self.pose_ = msg
            
    def vel_publisher_callback(self):
        if self.pose_ == None:
            return
                
        dist_x = self.target_x - self.pose_.x
        dist_y = self.target_y - self.pose_.y
        distance = math.sqrt(dist_x*dist_x + dist_y*dist_y)

        msg = Twist()
        if distance >0.5:
            msg.linear.x = 3*distance

            goal_theta = math.atan2(dist_y,dist_x)
            diff = goal_theta - self.pose_.theta
            if diff > math.pi:
                diff -= 2*math.pi
            elif diff < -math.pi:
                diff += 2*math.pi
            msg.angular.z = 0.5*diff
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
        
        self.vel_publisher.publish(msg)


     
     
def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()
     
     
if __name__ == "__main__":
    main()