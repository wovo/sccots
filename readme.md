# SCCOTS
# Standard Cboost Components Of The Shelve

## Summary

Sccots is a set of re-usable components 
for intelligent industrial automation
using docker and ROS2.

Docker containers are used to isolate dependencies 
for hardware items like cameras
that require manufacturer specific tools 
(drivers, SDKs) to be installed.

ROS2 is used to provide communication between docker containers.
This enables redeployment of AI processing and user interfaces.

The current sccots baseline is:

- Ubuntu 22.04 LTS (Jammy Jellyfish)
- ROS2 Humble Hawksbill
- x64 (intel), aarch64 (Raspberry Pi 4)



## ROS2

![ross2](pictures/ross2.png)

### Terminology

ROS stands for Robot Operating System, 
but it is neither an OS nor specifically for robots.
ROS is middleware for communication between nodes, 
which can be on the same host, or on different hosts within the
same network (and with a VPN, on different networks).
[[tinc](https://www.tinc-vpn.org/)]
[[husarnet](https://husarnet.com/blog/ros2-docker)]

ROS2 is the more same version of ROS, 
with unified C++ / Python interfaces on top of same C implementation.
The old ROS had functionality in the C++ and Python layers, 
which could behave differently.

ROS versions have cute names.
[Humble](https://docs.ros.org/en/humble/)
(Humble Hawksbill) is as of 2023 the latest version of ROS2.

### Communication

ROS nodes within a ROS domain communicate via named topics.
A topic has a single publisher node, and zero or more subscriber nodes.
A node can publish and subscribe to multiple topics.

A topic can be a message, a service, or an action.

A message is a one-way publish-subscribe communication:
the publisher has no direct interaction with the subscribers.
By default, messages are queued for each subscriber (up to a specified limit), 
so each subscriber will in the end receive all messages.

A service is a request-response communication.
A user node issues a request.
The server node responds with a response.

An action is like a service, but while the action is 
being executed the user gets updates.

DDS (Data Distribution Service) is the defaulkt protocol used
by ROS2 to distribute topics to ros nodes.

ROS can record the value of topics (including responses and updates??)
over time in a bag file.
A bag file can be played back for simulation, demo, debugging, etc.    

Messages, service requests, service responses, action requests,
action updates, and action results are all defined by ros interfaces.
An interface defines the type (structure) of the transferred data.
ROS has many pre-defined interfaces, for isntance for 
[camera images](http://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/Image.html).

By default, ros nodes in containers on the same host can communicate
with each other, but not with nodes containers on another host on the same network.
To enable communication over a network, add this to the docker run command
[[ref](https://answers.ros.org/question/358453/ros2-docker-multiple-hosts/)]:
```
--net=host --pid=host
```

package = collection of nodes, can have internal topics

parameter = configuration value for a node

node = participant in ROS communication

## USB camera

feh -Z -R 1 -Y
capture has a few seconds delay, but that seems to be the camera
@pi larger images are not received

## Spinnaker

## Terminology

topic
    distributed data
    ros2 topic 
        list
        info <topic>
        echo <topic> 
        pub <topic> <type> <data> --once --rate
        hz <topic>
    ros2 interface show <topic> 

## Raspberry Pi

- Raspberry Pi 4, 8 Gb memory, 32 Gb flash card
- Ubuntu 22.04, python 3.10.6
- download, flash, install takes ~ 1 hour (elapsed)
    
## Notes

- > 10 ms time domain
- installing ros-humble-desktop-full on Pi4 16 Gb gives errors
- include python3 in base
- migrate to https://git-lfs.com/
- ros nodes (in dockers) for:
    - gpio
    - camera
    - GUI
    - robot (arjun)
    - buisiness logic
    - sensors GPS, IMMU, Lidar /  profile-scanner, hyperspectral camera, 3D pointcloud 
    - actuators motor goto, updates, final
    - PLC 
    
ros node : a python or C++ object
ros application : a python or C++ application, 
docker container : can run a number of ros applications

https://www.ros.org/reps/rep-0145.html
https://github.com/ros-controls/ros2_control
https://control.ros.org/master/index.html
https://control.ros.org/master/doc/ros2_control/hardware_interface/doc/writing_new_hardware_interface.html
https://control.ros.org/master/doc/ros2_controllers/doc/controllers_index.html

sccots hardware interface
    service create <name>
        gpio <in,out,in_out,oc> <initial value> <specific>
            write <- 0 1 open
            read -> output 0, output 1, input 0, input 1
            publish?
        spi 
        i2c
        serial
            write -> string
            read <- string
            publish?
        keypad
        sensor        
        immu
    service list
    service delete    

https://docs.ros.org/en/crystal/Installation/Windows-Install-Binary.html#installing-prerequisites

https://github.com/ros2/common_interfaces

list service
create service
delete service <name>

<workspace-name> (a directory)
    src
        <package-name> (for some reason, inside src)
        
interfaces - services
    list <pattern>
    create <name> 
    delete <name>

    pin_direction
    pin_set
    pin_get    
    
interfaces - messages
    pin_change
    pin_rise
    pin_fall
    
==============================

windows
docker build github.com/wovo/sccots#main -f dockers/base -t work        
docker rm work
docker run --name work -it work
docker run --name work -v "C:\Wouter\cboost\sccots\work:/root/work" -it work


