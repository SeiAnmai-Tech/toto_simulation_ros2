import yaml
import cv2
import numpy as np

# Paths
input_image_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/h_world.pgm"
keep_out_zone_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/cr_keep_out_zone.yaml"
output_image_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/cr_image.pgm"
preferred_lanes_path = "/home/krushna/st/src/toto_simulation_ros2/toto2_description/maps/cr_preferred_lanes.yaml"

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

# Collect keep-out zones via terminal input
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

