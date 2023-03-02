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

## Docker

![docker](pictures/docker.png)

### Terminology

[docker glossary](https://docs.docker.com/glossary/)

A docker container is a running environment 
with its own file system, but sharing the OS kernel
with its host operating system and other docker images running on it.
A docker container starts its life as a copy (instance) 
of a docker image.

A docker file is the specification (blueprint) for creating a docker image.

The docker server is the entity that runs docker containers.
A docker server on Linux can run only Linux containers.
A docker server on Windows can be configured to run either
windows containers, or Linux containers (using WSL), but
not both at the same time. 
However, a container can run a VM, and that VM can run an OS that
is different from the host.
[[win vm in linux docker](https://medium.com/axon-technologies/installing-a-windows-virtual-machine-in-a-linux-docker-container-c78e4c3f9ba1)]
[[w10 enterprise](https://app.vagrantup.com/peru/boxes/windows-10-enterprise-x64-eval)]

### Installation

To install docker on Windows install the docker desktop.
Remember to restart it after a reboot.

To install docker on a fresh Ubuntu 22.04:

```
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y curl
sudo curl -sSL https://get.docker.com | sh
sudo docker version
```    
    
To enable docker use by a non-root user:

```
sudo usermod -aG docker <user-name>
```

### Build an image

The sccots repository provides a number of docker files:

- **base** (Ubuntu 22.04, ROS2 Humble)
- **spinnaker** (base + spinnaker camera)


To build a (local) image image-name from a sccots docker file file-name:

```
sudo docker build github.com/wovo/sccots#main -f docker/<file-name> -t <image-name>
```

Building an image is essentially installing software on a fresh system,
so it can take considerable time.
When building, docker saves the result of each step
(layer in docker terms), so a re-try or extension will essentially start 
from the first failed or changed step.

### Run a container interactively

To run an image that has been built in a new container, 
and get a shell to work in:

```
sudo docker run --name <container-name> -it <image-name>
 -v ~/work:/root/work 
 --device "/dev/bus/usb/001/021:/dev/bus/usb/001/021"
 --device "/dev/video0:/dev/video0"
```

When you leave the shell of a container it is stopped.
A stopped container maintains it state.
You can re-attached to a stopped container:

```
sudo docker restart <container-name>
sudo docker attach <container-name>
```

A stopped container occupies space on the file system.
To delete a container:

```
sudo docker rm -f <container-name>
```


### Using host resources

A container has its own file system.
You can provide access to elements of the host file system
when the container is created by adding
options to the docker run command.
For USB camera device, add 

```
--device "/dev/video0:/dev/video0"
```
For a working directory, add
 
```
-v ~/work:/root/work 
```

To claim more memory than the default, use for instance
```
-m=8g
```


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
A message is one-way:  the publisher has no direct interaction with
the subscribers.
A 

https://design.ros2.org/articles/interface_definition.html

DDS

ROS can record the value of topics over time in a bag file.
A bag file can be played back for simulation, demo, debugging, etc.    

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
    
    
image message
    http://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/Image.html

bag file
    timed recording of topics;
    can be played back for simulation, demo, debugging, etc.
    
## Notes

- installing ros-humble-desktop-full on Pi4 16 Gb gives errors
- include python3 in base
- migrate to https://git-lfs.com/