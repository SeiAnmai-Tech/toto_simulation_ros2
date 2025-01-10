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
        """Logic to update the PGM file."""
        self.get_logger().info("Updating PGM file...")
        # Add your PGM file modification logic here.
        # For now, just log the action.

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

