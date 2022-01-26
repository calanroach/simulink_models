#!/bin/bash 
 
##set the eth dev to 192.168.2.10 
##fix some parameters like buffers, enable jumbo frames 
## 
sudo ip addr add 192.168.2.10/24 dev enp2s0
#enable jumbo frame
sudo ip link set enp2s0 mtu 9000        
#kernel configs
sudo sysctl -w net.core.rmem_max=26214400
sudo sysctl -w net.core.rmem_default=26214400
sudo sysctl -w net.core.optmem_max=26214400
sudo sysctl -w net.core.optmem_max=26214400
sudo sysctl -w net.core.netdev_max_backlog=300000

#increase kernel buffers
sudo ethtool -G enp2s0 rx 4096
#sudo ethtool -K enp2s0 tx off rx on

#disable some feats that have been reported as problems in some nics
#sudo ethtool -K enp2s0 tso off
#sudo ethtool -K enp2s0 gro off lro off 

#increase the pci mmrbc, check https://glenewhittenberg.blogspot.com/2016/03/intel-x520-da2-performance-tuning-for.html
sudo setpci -v -d 8086:10fb e6.b=2e 

sudo ip link set up dev enp2s0
