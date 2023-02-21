import cv2

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from cv_bridge import CvBridge

from sensor_msgs.msg import Image
from std_msgs.msg import String

class MinimalPublisher(Node):
      def __init__(self):
         super().__init__('minimal_publisher')
         self.publisher_ = self.create_publisher(String, 'chatter_reply', 10)
         self.n = 0

      def respond( self ):
         self.n += 1
         msg = String()
         msg.data = 'Reply %d' % self.n )
         self.pubublisher.publish( msg )       

class Listener( Node ):

    def __init__(self, r):
        super().__init__('listener')
        self.r = r
        self.sub = self.create_subscription(
            Image, 
            'chatter_image', 
            self.chatter_callback, 
            10
        )
        self.publisher = self.create_publisher(
            String, 
            'chatter_reply', 
            10
        )        
        self.bridge = CvBridge()    
        self.n = 0
        print( "listening" )

    def chatter_callback(self, msg):
        img = self.bridge.imgmsg_to_cv2( msg, "bgr8" )    
        self.n += 1

        msg = String()
        msg.data = 'Reply %d' % self.n )
        self.pubublisher.publish( msg )         
        
        print( "image %d" % self.n )
        cv2.imwrite( "image.jpg", img )
        
        msg = String()
        msg.data = 'Reply %d' % self.n )
        self.pubublisher.publish( msg )        

def main(args=None):
    rclpy.init(args=args)

    node = Listener( r )
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        r.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()

