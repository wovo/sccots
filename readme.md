# SCCOTS
# Standard Cboost Components Of The Shelve

## Summary

Sccots provides re-usable components 
for intelligent industrial automation.

Docker containers are used to isolate dependencies 
for hardware items like cameras
that require manufacturer specific tools 
(drivers, SDKs) to be installed.

ROS2 is used to provide communication between docker containers.
This enables seamless redeployment of AI processing and user interfaces.

The current baseline:

- Ubuntu 22.04 LTS (Jammy Jellyfish)
- ROS2 Humble Hawksbill
- x64 (intel), aarch64 (Raspberry Pi 4)

## Docker

### Terminology

A docker container is a running environment, 
with its own file system, but sharing the OS kernel
with its host operating system and other docker images running on it.
A docker container starts its life as a copy (instance) 
of a docker image.

A docker image file is the specification for creating a docker image.

The docker server is the enity that runs docker containers.
A docker server on Linux can run only Linux containers.
A docker server on Windows can be configured to run either
windows containers, or Linux containers (using WSL), but
not both at the same time. 

### Install docker - Windows

To install docker on Windows:
    install docker desktop
    after each reboot: start it

### Install docker - Linux

To install docker on a fresh Ubuntu 22.04 
(this takes quite some time):

```
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y curl
sudo curl -sSL https://get.docker.com | sh
sudo docker version
```    
    
To enable docker use by a non-root user:

```
sudo usermod -aG docker <user_name>
```
    
To change the hotsname:

```
    sudo nano /etc/hostname
    sudo nano /etc/hosts
```

### Build a container

To build a container image from a sccots container file:

```
sudo docker build github.com/wovo/sccots#main -f containers/<file-name> -t <image-name>
```

Available as sccots container file-name:

- base: Ubuntu 22.04, ROS2 Humble
- spinnaker: base + spinnaker camera

### Run a container interactively

To run a container that has been built, and get a shell to work in:

```
sudo docker run --name work -it <image-name>
 -v ~/work:/root/work 
 --device "/dev/bus/usb/001/021:/dev/bus/usb/001/021"
 --device "/dev/video0:/dev/video0"
```

A container maintains state. 
You can 

sudo docker rm -f work; 
sudo docker run --name work -m=8g 
 -v ~/work:/root/work 
 --device "/dev/bus/usb/001/021:/dev/bus/usb/001/021"
 --device "/dev/video0:/dev/video0"
 -it sccots bash
 
docker run --name work -it sccots 
docker restart work
docker attach work
docker exec -it work /bin/sh 

## ROS2

### Terminology

ROS is Robot Operating System, but it is neither an OS nor specifically for robots.
ROS is middleware for communication between nodes, 
which can be on the same host, or on different hosts within the
same network (and with a VPN, on different networks).

ROS2 is the more same version of ROS, 
with unified C++ / Python interfaces on top of same C implementation.
The old ROS had functionality in the C++ and Python layers, 
which could behave differently.

ROS versions have cute names.
[Humble](https://docs.ros.org/en/humble/)
(Humble Hawksbill) is as of 2023 the latest version of ROS2.
    

## Terminology

ros2
    Ros = Robot Operating System, but it is neither an OS nor specifically for robots.
    Ros is middleware for communication between nodes, 
    which can be on the same host, or on different hosts within the
    same network (and with a vpn, on different networks).
    Ros2 is the more same version of ros, with
    unified thin C++ / Python interfaces on top of same C implementation.
    (The old ros had functionality in the C++ and Python layers, 
    which could behave differently.)
    
humble
    (Humble Hawksbill)
    https://docs.ros.org/en/humble/
    As of 2023 this is latest version of ros2.

topic
    distributed data
    ros2 topic 
        list
        info <topic>
        echo <topic> 
        pub <topic> <type> <data> --once --rate
        hz <topic>
    ros2 interface show <topic>    

interface
    communication between ros nodes.
    Can be by message, service or action
    https://design.ros2.org/articles/interface_definition.html
    
message
    ros one-way publish-subscribe (by default queued) inter-process communication interface
    .msg file describes a message
    in msg/ directory of a ROS package

service
    request / response interface
    .srv describes a service (request and response)
    
action 
    request - feedback - final interface
    
package  
    collection of nodes  

parameter
    configuration value for a node
    
node
    participant in ros(2) communication
    
image message
    http://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/Image.html

bag file
    timed recording of topics;
    can be played back for simulation, demo, debugging, etc.
    
    