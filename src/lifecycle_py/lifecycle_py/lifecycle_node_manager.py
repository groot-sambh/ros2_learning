#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
     
     
class LifecycleNodeManager(Node):
    def __init__(self):
        super().__init__("lifecycle_node_manager")
        self.declare_parameter("managed_node_name", rclpy.Parameter.Type.STRING)
        node_name = self.get_parameter("managed_node_name").value
        service_change_state_name
     
     
def main(args=None):
    rclpy.init(args=args)
    node = LifecycleNodeManager() # MODIFY NAME
   
    rclpy.shutdown()
     
     
if __name__ == "__main__":
    main()
