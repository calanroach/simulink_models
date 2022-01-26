# ROACH2 sensors codes

Some ROACH2 kernels dont allow you to ask for the sensor with the typical ?sensor-list; ?sensor-value katcp commands (like the kernel for the ROACH2 with a DRAM instantiation). In those cases we need to check kernel device values in the borph linux system in the powerpc.

The sensor are connected to a IIC bus and the devices get mapped into the /sys folder. To have an idea of which folder correspond to which sensor take a look to [this file.](https://github.com/casper-astro/katcp_devel/blob/master/tcpborphserver3/hwmon.c)

Temperature sensors: /sys/bus/i2c/devices/0-0018/
    -temp1_input: ambient temperature in millidegree
    -temp2_input: ppc temperature in millidegree
    -temp3_input: fpga temperature in millidegree

Fan chassis1:  /sys/bus/i2c/devices/0-001b
    -fan1_input: fan speed, in rpm

Fan chassis2: /sys/bus/i2c/devices/0-001f
    -fan1_input

##TODO
- [x] Make scripts to measure temperature in the RAOCH2 DRAM kernel.
- [ ] Make scripts to measure temperature in the default ROACH2 kernel.
