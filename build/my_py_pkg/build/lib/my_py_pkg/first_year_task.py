    #!/usr/bin/env python3
    import rclpy
    from rclpy.node import Node
    from example_interfaces.msg import Int32
     
    class TestNode(Node): # MODIFY NAME
        def __init__(self):
            super().__init__("test_node") # MODIFY NAME
            self.subscriber = self.create_subscription(Int32, "number", self.subscriber_callback)

        def subscriber_callback(self, msg):
            self.get_logger().info(str(msg.data))
     
     
    def main(args=None):
        rclpy.init(args=args)
        node = TestNode() # MODIFY NAME
        rclpy.spin(node)
        rclpy.shutdown()
     
     
    if __name__ == "__main__":
        main()