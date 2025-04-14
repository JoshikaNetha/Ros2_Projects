from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os

def generate_launch_description():
    # Assuming the workspace is sourced and installed path is correct
    gui_node_path = os.path.join(
        os.getenv('AMENT_PREFIX_PATH').split(':')[0],
        'lib',
        'pyqt_test',
        'scripts',
        'main.py'
    )

    return LaunchDescription([
        # C++ node
        # Node(
        #     package='pyqt_test',
        #     executable='pyqt_test_node',  # Must match the executable name in CMake
        #     name='cpp_node',
        #     output='screen'
        # ),

        # Python PyQt GUI node
        ExecuteProcess(
            cmd=['python3', gui_node_path],
            name='pyqt_gui_node',
            output='screen'
        )
    ])
