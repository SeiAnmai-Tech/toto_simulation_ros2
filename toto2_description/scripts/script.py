import yaml
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from nav2_msgs.srv import LoadMap
from std_srvs.srv import Empty
import os
from datetime import datetime
import shutil

class MapUpdater(Node):
    def __init__(self):
        super().__init__('map_updater')

        # Service clients
        self.load_map_client = self.create_client(LoadMap, '/map_server/load_map')
        self.clear_costmaps_client = self.create_client(Empty, '/local_costmap/clear')

        # Wait for the map server to be available
        while not self.load_map_client.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Waiting for the map server to be available...')
        self.get_logger().info('Map server is available.')

        # Check for the clear costmap service
        if not self.clear_costmaps_client.wait_for_service(timeout_sec=5.0):
            self.get_logger().warning("Clear costmaps service unavailable, proceeding without it.")
        else:
            self.get_logger().info('Clear costmap service is available.')

        # Define file paths
        self.yaml_file_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/preffed_lanes.yaml"
        self.pgm_file_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/cr_image.pgm"

        # Ensure the files exist
        if not os.path.exists(self.yaml_file_path):
            self.get_logger().error(f"YAML file does not exist: {self.yaml_file_path}")
            return
        if not os.path.exists(self.pgm_file_path):
            self.get_logger().error(f"PGM file does not exist: {self.pgm_file_path}")
            return

        # Backup the existing PGM file
        self.backup_pgm_file()

        # Update the PGM file
        self.update_pgm_file()

        # Clear previous map and reload the new one
        self.clear_costmaps()
        self.reload_map()

    def backup_pgm_file(self):
        """Creates a backup of the existing PGM file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{self.pgm_file_path}_backup_{timestamp}"
        shutil.copy2(self.pgm_file_path, backup_path)
        self.get_logger().info(f"Backup of PGM file created: {backup_path}")

    def update_pgm_file(self):
        """Logic to update the PGM file with keep-out zones and preferred lanes."""
        self.get_logger().info("Updating PGM file...")
        
        # Paths
        input_image_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/h_world.pgm"
        keep_out_zone_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/cr_keep_out_zone.yaml"
        output_image_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/cr_image.pgm"
        preferred_lanes_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/cr_preferred_lanes.yaml"

        # Map dimensions in meters
        map_width_m = 5.0  # Width of the map in meters
        map_height_m = 4.0  # Height of the map in meters

        # Image dimensions in pixels
        image_width_px = 506
        image_height_px = 394

        # Conversion factors
        scale_x = image_width_px / map_width_m
        scale_y = image_height_px / map_height_m

        # Load the input image
        input_image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
        if input_image is None:
            raise FileNotFoundError(f"Input image not found at {input_image_path}")

        # Collect keep-out zones
        keep_out_zones = []
        while True:
            zone_name = input("Enter the name of the keep-out zone (or 'done' to finish): ").strip()
            if zone_name.lower() == "done":
                break

            points = []
            print(f"Enter points for {zone_name} (format: x y). Type 'end' to finish this zone.")
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
                keep_out_zones.append({"name": zone_name, "points": points})

        # Save the keep-out zones to YAML
        keep_out_data = {"keep_out_zones": keep_out_zones}
        with open(keep_out_zone_path, 'w') as file:
            yaml.safe_dump(keep_out_data, file)
        print(f"Keep-out zones saved to {keep_out_zone_path}")

        # Create a copy of the image to draw on
        output_image = input_image.copy()

        # Process each zone in the keep-out zones
        for zone in keep_out_zones:
            # Extract the polygon points and convert to pixel coordinates
            points = [
                (
                    int(point["x"] * scale_x),  # Scale x-coordinate
                    int((map_height_m - point["y"]) * scale_y)  # Scale and flip y-coordinate
                )
                for point in zone["points"]
            ]
            points = np.array(points, dtype=np.int32)
            points = points.reshape((-1, 1, 2))

            # Draw the polygon with black color (value 0) and fill it
            cv2.fillPoly(output_image, [points], color=0)

        # Save the output image
        cv2.imwrite(output_image_path, output_image)
        print(f"Output image saved to {output_image_path}")

        # Generate preferred_lanes.yaml (example data)
        preferred_lanes = {
            "preferred_lanes": [
                {"id": 1, "description": "Example lane for reference"}
            ]
        }

        with open(preferred_lanes_path, 'w') as file:
            yaml.safe_dump(preferred_lanes, file)

        print(f"Preferred lanes saved to {preferred_lanes_path}")

    def clear_costmaps(self):
        """Clears the existing costmaps to ensure no collisions."""
        self.get_logger().info("Clearing costmaps...")
        if self.clear_costmaps_client.wait_for_service(timeout_sec=5.0):
            request = Empty.Request()
            future = self.clear_costmaps_client.call_async(request)
            rclpy.spin_until_future_complete(self, future)
            if future.result() is not None:
                self.get_logger().info("Costmaps cleared successfully.")
            else:
                self.get_logger().error(f"Failed to clear costmaps: {future.exception()}")
        else:
            self.get_logger().warning("Clear costmaps service unavailable, skipping...")

    def reload_map(self):
        """Reloads the map using the Nav2 LoadMap service."""
        request = LoadMap.Request()
        request.map_url = self.yaml_file_path

        self.get_logger().info(f"Attempting to load map from: {request.map_url}")
        future = self.load_map_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            response = future.result()
            if hasattr(response, 'result') and response.result == 0:
                self.get_logger().info('Map successfully reloaded!')
            else:
                self.get_logger().error(f"Failed to reload map. Error code: {response.result}")
        else:
            self.get_logger().error(f"Service call failed: {future.exception()}")

def main(args=None):
    rclpy.init(args=args)
    map_updater = MapUpdater()
    rclpy.spin(map_updater)
    map_updater.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

