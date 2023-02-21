import rclpy
import rclpy.node
# from rclpy.node import Node
# from std_msgs.msg import String
import std_msgs
import std_msgs.msg
#from cv_bridge import CvBridge
import cv_bridge
# from sensor_msgs.msg import Image
import sensor_msgs
import sensor_msgs.msg
import cv2
import numpy
import time

class camera_talker( rclpy.node.Node ):

    def __init__(self):
        rclpy.node.Node.__init__( self, "camera_talker" )
        
        self.publisher = self.create_publisher( 
            sensor_msgs.msg.Image, 
            'chatter_image', 
            10
        )
         
        self.timer = self.create_timer( 
            5, 
            self.post_image 
        )
        
        #print( self.create_subscription.__doc__ )
        
        self.sub = self.create_subscription(
            msg_type = std_msgs.msg.String, 
            topic = 'chatter_reply', 
            callback = self.reply_callback, 
            qos_profile = 10
        )          
        
        self.bridge = cv_bridge.CvBridge()
        self.n = 0
        
        self.camera = cv2.VideoCapture( '/dev/video0', cv2.CAP_V4L)
        self.camera.set( cv2.CAP_PROP_FRAME_WIDTH, 128 )
        self.camera.set( cv2.CAP_PROP_FRAME_HEIGHT, 128 )        

    def post_image( self ):
        ret, image = self.camera.read() 
        self.t1 = time.time_ns()
        self.publisher.publish(
            self.bridge.cv2_to_imgmsg( numpy.array( image ), "bgr8" )
        )
        self.n += 1
        print( 'Published image %d' % self.n )
         
    def reply_callback( self, msg ):
        t2 = time.time_ns()
        print( 'I heard: [%s]' % msg.data )
        print( '    round trip %f ms' % ( ( t2 - self.t1 ) / 1_000_000.0 ) )

def main(args=None):
    rclpy.init( args = args )
    camera = camera_talker()
    rclpy.spin( camera )
    camera.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
   main()
