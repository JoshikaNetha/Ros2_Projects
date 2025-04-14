from ament_index_python.packages import get_package_prefix

try:
    print(get_package_prefix('turtle_tf2_py'))
except Exception as e:
    print(f"Package not found: {e}")

