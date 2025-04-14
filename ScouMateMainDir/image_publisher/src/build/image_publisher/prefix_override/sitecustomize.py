import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/joshikanamani/Ros2/ScouMateMainDir/image_publisher/src/install/image_publisher'
