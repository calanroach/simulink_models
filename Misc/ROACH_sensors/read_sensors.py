import telnetlib, os, time


def roach_connect(roach_ip, sleep_time=0.5):
    user = 'root'
    tn = telnetlib.Telnet(roach_ip)
    tn.read_until("login: ")
    tn.write(user + "\n")
    time.sleep(sleep_time)
    tn.read_very_eager()
    time.sleep(sleep_time)
    return tn

def read_ambient_temp(roach_ip, sleep_time=0.5):
    """Read the ambient temperature in degrees
    """
    tn = roach_connect(roach_ip, sleep_time=sleep_time)
    #tn.write('cat /sys/bus/i2c/devices/0-0018/temp1_input \n')
    tn.write('cat /sys/bus/i2c/devices/0-0018/hwmon/hwmon4/temp1_input \n')
    time.sleep(sleep_time)
    ans = tn.read_very_eager()
    time.sleep(sleep_time)
    tn.close()
    temp = float(ans.split('\r\n')[1])
    temp /= 1000.
    return temp


def read_ppc_temp(roach_ip, sleep_time=0.5):
    """Read the Powerpc temperature in degrees
    """
    tn = roach_connect(roach_ip, sleep_time=sleep_time)
    #tn.write('cat /sys/bus/i2c/devices/0-0018/temp2_input \n')
    tn.write('cat /sys/bus/i2c/devices/0-0018/hwmon/hwmon4/temp2_input \n')
    time.sleep(sleep_time)
    ans = tn.read_very_eager()
    time.sleep(sleep_time)
    tn.close()
    temp = float(ans.split('\r\n')[1])
    temp /= 1000.
    return temp

def read_fpga_temp(roach_ip, sleep_time=0.5):
    """Read the ambient temperature in degrees
    """
    tn = roach_connect(roach_ip, sleep_time=sleep_time)
    #tn.write('cat /sys/bus/i2c/devices/0-0018/temp3_input \n')
    tn.write('cat /sys/bus/i2c/devices/0-0018/hwmon/hwmon4/temp3_input \n')
    time.sleep(sleep_time)
    ans = tn.read_very_eager()
    time.sleep(sleep_time)
    tn.close()
    temp = float(ans.split('\r\n')[1])
    temp /= 1000.
    return temp
