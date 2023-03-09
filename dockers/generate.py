# ============================================================================
#
# generate the docker files
#
# ============================================================================   

class component:
    def __init__( self, description, lines ):
        self.description = description
        self.lines = lines  

# ============================================================================   

ubuntu = component( 
    "unbuntu 22.04 LTS (jammy)",
    """
        FROM ubuntu:22.04

        # update & upgrade
        RUN apt update
        RUN apt upgrade -y    
        
        # for apt to be noninteractive
        ENV DEBIAN_FRONTEND noninteractive
        ENV DEBCONF_NONINTERACTIVE_SEEN true
        
        # locales
        RUN apt update 
        RUN apt install -y locales
        RUN locale-gen en_US en_US.UTF-8
        RUN update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8      
    """
)    

# ============================================================================   

python = component( 
    "Python",
    """
        RUN apt install -y python3
        RUN apt install -y pip
        WORKDIR /root
        RUN echo "alias python=python3" >> .bashrc
        RUN echo "alias p=python3" >> .bashrc 
    """
)  

# ============================================================================   

cpp = component( 
    "C++",
    """
        RUN apt install -y build-essential
        RUN apt install -y manpages-dev      
    """
)  

# ============================================================================   

ros = component( 
    "ROS2 humble ",
    """
        RUN apt install -y locales
        RUN locale-gen en_US en_US.UTF-8
        RUN update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
        # export LANG=en_US.UTF-8
        
        # magic to get the ros repository
        # https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html
        # add extra update at the end
        RUN apt install -y software-properties-common
        RUN add-apt-repository universe
        RUN apt update 
        RUN apt install -y curl
        RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
        RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null
        RUN apt upgrade -y
        RUN apt update
        
        # install ros humble
        # https://devanshdhrafani.github.io/blog/2021/04/15/dockerros2.html
        # desktop-full is installed, this might be overkill
        RUN apt install -y ros-humble-desktop
        RUN apt install -y ros-dev-tools
        # included in above, maybe needed with a smaller base install 
        RUN apt install -y python3-colcon-common-extensions   
    """
)  

# ============================================================================   

spinnaker = component( 
    "Spinnaker FLIR camera environment",
    """
        # install spinnaker python
        # https://pypi.org/project/simple-pyspin/
        WORKDIR /root/temp
        RUN apt install -y git pip
        RUN pip install --upgrade numpy matplotlib
        # pillow for python 3.10
        RUN pip install Pillow==9.2.0
        RUN git clone https://github.com/wovo/spinnaker
        RUN mv spinnaker/ubuntu2204/python/spinnaker_python-3.0.0.118-cp310-cp310-linux_x86_64.tar.gz sppy.tar.gz
        RUN tar -xzf sppy.tar.gz
        RUN pip install *.whl
        RUN pip install simple-pyspin
        
        # install spinnaker drivers
        WORKDIR /root/temp
        RUN mv spinnaker/ubuntu2204/spinnaker-3.0.0.118-amd64-pkg.tar.gz sp.tar.gz
        RUN tar -xzf sp.tar.gz
        WORKDIR /root/temp/spinnaker-3.0.0.118-amd64
        # modified scripts that runs noninteractive
        # and prime for the ula to be accepted
        RUN apt install -y debconf-utils
        RUN cp ../spinnaker/ubuntu2204/install_spinnaker.sh .
        RUN echo "libgentl libspinnaker/accepted-flir-eula select true" | debconf-set-selections
        RUN bash install_spinnaker.sh   
    """
)  

# ============================================================================   

shell = component( 
    "bash login shell",
    """
        WORKDIR /root
        RUN echo "echo sccots environment: <<name>>" >> .bashrc
        CMD [ "bash" ]  
    """
)  

# ============================================================================   

bar = "# " + 76 * "=" + "\n" 

def create( name, components ):
    with open( name, "w" ) as f:
        f.write( bar )
        f.write( "#\n" )
        f.write( "# sccots container file %s\n" % name )
        f.write( "#\n" )
        f.write( "# This is a generated file.\n" )
        f.write( "#\n" )
        f.write( bar )
        f.write( "#\n" )
        for c in components:
            f.write( "\n" )
            f.write( bar )
            f.write( "#\n" )
            f.write( "# %s\n" % c.description )
            f.write( "#\n" )
            f.write( bar )
            for line in c.lines.split( "\n" ):
                f.write( line.lstrip().replace( "<<name>>", name ) + "\n" )
            
def main():
    for f, c in (
        ( "ubuntu", ( ubuntu, shell ) ),
        ( "develop", ( ubuntu, python, cpp, shell ) ),
        ( "ros", ( ubuntu, python, cpp, ros, shell ) ),
        ( "spinnaker", ( ubuntu, python, cpp, ros, spinnaker, shell ) ),
    ):    
        create( f, c )

if __name__ == "__main__":
    main()
    print( "Docker files generated.\n" )
    print( "Don't forget to push to git.\n" )

# ============================================================================   
