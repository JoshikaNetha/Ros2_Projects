import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('img_pub')
        self.pub4 = self.create_publisher(Image, '/cam1/image_raw', 10)
        self.pub1 = self.create_publisher(Image, '/cam2/image_raw', 10)
        self.pub2 = self.create_publisher(Image, '/cam3/image_raw', 10)
        self.pub3 = self.create_publisher(Image, '/cam4/image_raw', 10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.bridge = CvBridge()
        self.image = cv2.imread('/home/joshikanamani/Downloads/passport_photo.png')

    def timer_callback(self):
        msg = self.bridge.cv2_to_imgmsg(self.image, encoding='bgr8')
        self.pub1.publish(msg)
        self.pub2.publish(msg)
        self.pub3.publish(msg)
        self.pub4.publish(msg)

rclpy.init()
node = ImagePublisher()
rclpy.spin(node)
node.destroy_node()
rclpy.shutdown()
