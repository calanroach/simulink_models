#Ten Gbe models

##Info
To use the 10Gbe interface correctly you need to tweak your NIC. The init_tge.sh script sets the ep2s0 with the ip 192.168.2.10 and make some adjustments for some linux options. You need to have installed ethtool and obviously you need the right driver for your NIC.

For the last instruction (setpci) you need to look for the pci id of the NIC device (in the default code is 8086:10fbe)

##TODO
- [x] Loopback.
- [ ] Packetize and send spectrometers.
    - [ ] 2input spectrometer
    - [ ] 4input spectrometer
- [ ] Packetize and send correlators output.
    - [ ] 2input correlator
    - [ ] 4input correlator
- [ ] Packetize and send raw ADC data. 
- [ ] Process the raw ADC data using a GPU.

