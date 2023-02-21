import rclpy
# from rclpy.node import Node
# from std_msgs.msg import String
import std_msgs
#from cv_bridge import CvBridge
import cv_bridge
# from sensor_msgs.msg import Image
import sensor_msgs
import cv2
import numpy
import time

class camera_talker( rclpy.node.Node ):

    def __init__(self):
        rclpy.node.Node.__init__( self, "camera talker" )
        
        self.publisher = self.create_publisher( 
            sensor_msgs.msg.Image, 
            'chatter_image', 
            10
        )
         
        self.timer = self.create_timer( 
            1, 
            self.post_image 
        )
        
        self.sub = self.create_subscription(
            String, 
            'chatter_reply', 
            self.reply_callback, 
            10
        )          
        
        self.bridge = cv_bridge.CvBridge()
        self.n = 0
        
        self.camera = cv2.VideoCapture( '/dev/video0', cv2.CAP_V4L)
        self.camera.set( cv2.CAP_PROP_FRAME_WIDTH, 128 )
        self.camera.set( cv2.CAP_PROP_FRAME_HEIGHT, 128 )        

      def post_image( self ):
         ret, image = self.camera.read() 
         self.publisher.publish(
             self.bridge.cv2_to_imgmsg( numpy.array( image ), "bgr8" )
         )
         self.n += 1
         self.t1 = time.time_ns()
         print( 'Published image %d' % self.n )
         
    def reply_callback( self, msg ):
        t2 = time.time_ns()
        print( 'I heard: [%s]' % msg.data )
        print( '    round trip %d' % t2 - self.t1

def main(args=None):
    rclpy.init( args = args )
    camera = camera_talker()
    rclpy.spin( camera )
    camera.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
   main()
