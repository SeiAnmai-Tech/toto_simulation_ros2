import yaml
import cv2
import numpy as np

# Paths
input_image_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/h_world.pgm"
keep_out_zone_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/keep_out_zone.yaml"
output_image_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/output_image.pgm"
preferred_lanes_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/preferred_lanes.yaml"

# Map dimensions in meters (assumed to match the map metadata)
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

# Load the keep_out_zone.yaml file
with open(keep_out_zone_path, 'r') as file:
    keep_out_data = yaml.safe_load(file)

# Create a copy of the image to draw on
output_image = input_image.copy()

# Process each zone in the keep_out_zone.yaml
for zone in keep_out_data.get("keep_out_zones", []):
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

