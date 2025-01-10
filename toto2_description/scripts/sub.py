import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped  # Adjust based on your message type

class PointsSubscriber(Node):
    def __init__(self):
        super().__init__('points_subscriber')
        self.subscription = self.create_subscription(
            PointStamped,  # Adjust based on the message type
            '/updated_map',
            self.points_callback,
            10
        )
        self.get_logger().info('Subscribed to /updated_map')

    def points_callback(self, msg):
        self.get_logger().info(f'Received point: {msg.point}')
        # Process the point and integrate into navigation

def main(args=None):
    rclpy.init(args=args)
    node = PointsSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

