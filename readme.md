# SCCOTS : Standard Cboost Components Of The Shelve

-----------------------------------------------------------------------------

## Summary

Sccots provides re-usable components 
for intelligent industrial automation.

Docker containers are used to isolate dependencies 
for hardware items like cameras
that require manufacturer specific tools 
(drivers, SDKs) to be installed.

ROS2 is used to provide communication between docker nodes.
This enables seamless redeployment of AI processing and user interfaces.

The current baseline:

- Ubuntu 22.04 LTS (Jammy Jellyfish)
- ROS2 Humble Hawksbill
- x64 (intel), aarch64 (Raspberry Pi 4)

-----------------------------------------------------------------------------

## Docker

### Install docker - Windows

To install dcoker on Windows:
    install docker desktop
    after each reboot: start it

### Install docker - Linux

To install docker on a fresh Ubuntu 22.04 
(this takes quite some time):

```
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get intsall -y curl
curl -sSL https://get.docker.com | sh
docker version
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
    
-----------------------------------------------------------------------------
    
    