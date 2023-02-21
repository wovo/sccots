# ===========================================================================
#
# scotts
#
# ===========================================================================

import rclpy

class listener( Node ):

class subscriber 



from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import numpy as np

# open camera
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)

# set dimensions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

class Listener(Node):

    def __init__(self, p ):
        super().__init__('listener')
        self.p = p
        self.sub = self.create_subscription(String, 'chatter_reply', self.chatter_callback, 10)  
        print( "listening" )

    def chatter_callback(self, msg):
        p.reply()

class MinimalPublisher(Node):
      def __init__(self, l):
         super().__init__('minimal_publisher')
         self.l = l
         self.publisher_ = self.create_publisher(Image, 'chatter_image', 10)
         self.timer = self.create_timer( 5, self.timer_callback)
         self.cv_image = cv2.imread('test.jpg') ### an RGB image 
         self.bridge = CvBridge()
         self.n = 0
         
      def reply( self ):
                

      def timer_callback(self):
         ret, im = cap.read() 
         self.publisher_.publish(self.bridge.cv2_to_imgmsg(np.array(im), "bgr8"))
         self.n += 1
         print( 'Published image %d' % self.n )

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher( l )
    l = Listener( minimal_publisher )
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    l.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
   main()
