import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
import yaml
import cv2
import numpy as np

# Paths
input_image_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/h_world.pgm"
keep_out_zone_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/pub_keep_out_zone.yaml"
output_image_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/pub_image.pgm"

# Map dimensions in meters (assumed to match the map metadata)
map_width_m = 5.0  # Width of the map in meters
map_height_m = 4.0  # Height of the map in meters

# Image dimensions in pixels
image_width_px = 506
image_height_px = 394

# Conversion factors
scale_x = image_width_px / map_width_m
scale_y = image_height_px / map_height_m

class PointsPublisher(Node):
    def __init__(self):
        super().__init__("points_publisher")
        self.topic_publishers = {}

    def create_publisher_for_topic(self, topic_name):
        if topic_name not in self.topic_publishers:
            self.topic_publishers[topic_name] = self.create_publisher(Point, topic_name, 10)
            self.get_logger().info(f"Publisher created for topic: {topic_name}")

    def publish_points(self, topic_name, points):
        for point in points:
            msg = Point()
            msg.x = point["x"]
            msg.y = point["y"]
            msg.z = 0.0  # Assuming 2D points, set z to 0
            self.topic_publishers[topic_name].publish(msg)
            self.get_logger().info(f"Published point ({msg.x}, {msg.y}, {msg.z}) to {topic_name}")

def main():
    rclpy.init()
    node = PointsPublisher()

    # Load the input image
    input_image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    if input_image is None:
        raise FileNotFoundError(f"Input image not found at {input_image_path}")

    # Create a copy of the image to draw on
    output_image = input_image.copy()

    # Collect points for topics via terminal input
    keep_out_zones = {}

    while True:
        topic_name = input("Enter the name of the topic (e.g., /points1, /points2 or 'done' to finish): ").strip()
        if topic_name.lower() == "done":
            break
        
        node.create_publisher_for_topic(topic_name)

        points = []
        print(f"Enter points for {topic_name} (format: x y). Type 'end' to finish this topic.")
        while True:
            point_input = input("Enter point: ").strip()
            if point_input.lower() == "end":
                break
            
            try:
                x, y = map(float, point_input.split())
                points.append({"x": x, "y": y})
            except ValueError:
                print("Invalid input. Please enter coordinates in the format: x y")

        if points:
            keep_out_zones[topic_name] = points
            node.publish_points(topic_name, points)

    # Process each topic
    for topic, points in keep_out_zones.items():
        # Convert points to pixel coordinates and draw on the image
        pixel_points = [
            (
                int(point["x"] * scale_x),  # Scale x-coordinate
                int((map_height_m - point["y"]) * scale_y)  # Scale and flip y-coordinate
            )
            for point in points
        ]
        pixel_points = np.array(pixel_points, dtype=np.int32).reshape((-1, 1, 2))
        
        # Draw the polygon with black color (value 0) and fill it
        cv2.fillPoly(output_image, [pixel_points], color=0)

    # Save the output image
    cv2.imwrite(output_image_path, output_image)
    print(f"Output image saved to {output_image_path}")

    # Save the keep-out zones to YAML
    keep_out_data = {"keep_out_zones": keep_out_zones}
    with open(keep_out_zone_path, 'w') as file:
        yaml.safe_dump(keep_out_data, file)
    print(f"Keep-out zones saved to {keep_out_zone_path}")

    # Shutdown the node after processing
    node.destroy_node()
    rclpy.shutdown()
    print("Node shut down. Map generation complete.")

if __name__ == "__main__":
    main()

