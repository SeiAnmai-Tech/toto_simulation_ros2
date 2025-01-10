cmake_minimum_required(VERSION 3.5)
project(toto2_description)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)

# Install directories for config, launch, maps, meshes, models, params, rviz, src, worlds
install(
  DIRECTORY config launch maps meshes models params rviz src worlds
  DESTINATION share/${PROJECT_NAME}
)

# Install your keep_out.py script
install(
  PROGRAMS
  scripts/keep_out.py  # Update the path if your script is located elsewhere
  DESTINATION lib/${PROJECT_NAME}
)

# Install your cr.py script
install(
  PROGRAMS
  scripts/cr.py  # Update the path if your script is located elsewhere
  DESTINATION lib/${PROJECT_NAME}
)

# Install any other necessary scripts or executables here
# For example, if you have another script to install:
# install(
#   PROGRAMS
#   scripts/another_script.py
#   DESTINATION lib/${PROJECT_NAME}
# )

# Testing dependencies
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  # set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  # set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
