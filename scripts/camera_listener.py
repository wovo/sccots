import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2

from std_msgs.msg import String


class Listener(Node):

    def __init__(self):
        super().__init__('listener')
        self.sub = self.create_subscription(Image, 'chatter_image', self.chatter_callback, 10)
        self.bridge = CvBridge()    
        self.n = 0
        print( "listening" )

    def chatter_callback(self, msg):
        img = self.bridge.imgmsg_to_cv2( msg, "bgr8")    
        self.n += 1
        print( "image %d" % self.n )
        cv2.imwrite( "image.jpg", img )


def main(args=None):
    rclpy.init(args=args)

    node = Listener()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()

