# =========================================================================== 
#
# sccots ros2hw server and tool
#    
# =========================================================================== 
    
import sys
import time

import rclpy
import rclpy.node
import std_msgs
import std_msgs.msg

# =========================================================================== 
    
class server( rclpy.node.Node ):

    def __init__(self):
        rclpy.node.Node.__init__( self, name )
        
        self.publisher = self.create_publisher( 
            sensor_msgs.msg.Image, 
            "%s-list" % name, 
            10
        )         
        
        self.bridge = cv_bridge.CvBridge()
        self.n = 0
        
        self.command_list = self.create_service( 
            AddTwoInts, 
            'add_two_ints', 
            self.add_two_ints_callback 
        )

    def add_two_ints_callback( self, request, response ):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))

        return response        

# =========================================================================== 
    
def run_server( name: str ):
    rclpy.init()        
    node = server( name )
    try:
        rclpy.spin( node )
    except ( KeyboardInterrupt, ExternalShutdownException ):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
    
# =========================================================================== 

def commmand_list( name: str ):
    rclpy.init()
    rclpy.shutdown()  
    
    
# =========================================================================== 
    
def main( args ):
    print( args )
    if len( args ) < 2:
        print( "help" )    
        return
        
        
    command = args[ 1 ]    
    name = args[ 2 ]
    
    if command == "server":
        run_server( name = name )
        
    elif command == "list":
        command_list( name = name )

    elif command == "make":
        command_make( name = name )      

# =========================================================================== 
    
if __name__ == '__main__':
   main( sys.argv )

# =========================================================================== 
    
