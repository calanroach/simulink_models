import matplotlib.pyplot as plt
import numpy as np
import ipdb

d0 = 'dout0.txt'
d1 = 'dout1.txt'

fs = 24.5
fft_len = 512

##read the first lo
#ideal
lo_dir = 'lo_79/'
lo = 79.2

iters = 23
freq_ideal_0 = np.arange(iters)+67.2

index = np.around((freq_ideal_0-lo)/fs*fft_len)
index = np.abs(index).astype(int)

lsb_ideal_0 = np.zeros(iters-1)
usb_ideal_0 = np.zeros(iters-1)
for i in range(1,iters):
    d0_name = lo_dir+'ideal/'+str(i)+d0;
    d1_name = lo_dir+'ideal/'+str(i)+d1
    dout0 = np.loadtxt(d0_name, delimiter=',')
    dout1 = np.loadtxt(d1_name, delimiter=',')
    ind = index[i-1]
    #ind = np.argmax(dout0[:, 2])
    usb_ideal_0[i-1] = 10*np.log10(dout0[ind,2]+1)
    lsb_ideal_0[i-1] = 10*np.log10(dout1[ind,2]+1)

#srr_lsb = lsb_ideal_0[:len(freq_ideal_0)/2]-usb_ideal_0[:len(freq_ideal_0)/2]
#srr_usb = usb_ideal_0[len(freq_ideal_0)/2+1:]-lsb_ideal_0[len(freq_ideal_0)/2+1:]
aux = len(freq_ideal_0)/2
#ipdb.set_trace()
#srr_lsb = lsb_ideal_0[:aux]-usb_ideal_0[:aux]
#srr_usb = lsb_ideal_0[aux+1:]-usb_ideal_0[aux+1:]
srr_ideal_0 = np.abs(lsb_ideal_0-usb_ideal_0)
srr_ideal_0 = np.hstack([srr_ideal_0[:aux+1], srr_ideal_0[aux+2:]])
freq_ideal_0 = np.hstack([freq_ideal_0[:aux], freq_ideal_0[aux+1:]])
plt.plot(freq_ideal_0[:-1], srr_ideal_0, 'bo-', label='ideal')

#plt.plot(freq_ideal_0[:aux], srr_lsb, 'bo-', label='ideal')
#plt.plot(freq_ideal_0[aux+1:], srr_usb, 'bo-')

#calibrated
iters = 25
freq_cal_0 = np.arange(iters)+67.2

index = np.around((freq_cal_0-lo)/fs*fft_len)
index = np.abs(index).astype(int)

lsb_cal_0 = np.zeros(iters-1)
usb_cal_0 = np.zeros(iters-1)
for i in range(1,iters):
    d0_name = lo_dir+'test/'+str(i)+d0;
    d1_name = lo_dir+'test/'+str(i)+d1
    dout0 = np.loadtxt(d0_name, delimiter=',')
    dout1 = np.loadtxt(d1_name, delimiter=',')
    ind = index[i-1]
    #ind = np.argmax(dout0[:, 2])
    usb_cal_0[i-1] = 10*np.log10(dout0[ind,2]+1)
    lsb_cal_0[i-1] = 10*np.log10(dout1[ind,2]+1)

aux = len(freq_cal_0)/2
srr_cal_0 = np.abs(lsb_cal_0-usb_cal_0)
srr_cal_0 = np.hstack([srr_cal_0[:aux], srr_cal_0[aux+1:]])
freq_cal_0 = np.hstack([freq_cal_0[:aux], freq_cal_0[aux+1:]])
plt.plot(freq_cal_0[:-1], srr_cal_0, 'r*-', label='calibrated')

#srr_lsb = lsb_cal_0[:aux]-usb_cal_0[:aux]
#srr_usb = lsb_cal_0[aux+1:]-usb_cal_0[aux+1:]
#plt.plot(freq_cal_0[:aux], srr_lsb, 'r*-', label='calibrated')
#plt.plot(freq_cal_0[aux+1:], srr_usb, 'r*-')

##lo2
lo_dir = 'lo_103/'
lo = 103.8

iters = 25
freq_ideal_1 = np.arange(iters)+91.8

index = np.around((freq_ideal_1-lo)/fs*fft_len)
index = np.abs(index).astype(int)

lsb_ideal_1 = np.zeros(iters-1)
usb_ideal_1 = np.zeros(iters-1)
for i in range(1,iters):
    d0_name = lo_dir+'ideal/'+str(i)+d0;
    d1_name = lo_dir+'ideal/'+str(i)+d1
    dout0 = np.loadtxt(d0_name, delimiter=',')
    dout1 = np.loadtxt(d1_name, delimiter=',')
    ind = index[i-1]
    #ind = np.argmax(dout0[:, 2])
    usb_ideal_1[i-1] = 10*np.log10(dout0[ind,2]+1)
    lsb_ideal_1[i-1] = 10*np.log10(dout1[ind,2]+1)


aux = len(freq_ideal_1)/2
srr_ideal_1 = np.abs(lsb_ideal_1-usb_ideal_1)
srr_ideal_1 = np.hstack([srr_ideal_1[:aux], srr_ideal_1[aux+1:]])
freq_ideal_1 = np.hstack([freq_ideal_1[:aux], freq_ideal_1[aux+1:]])
plt.plot(freq_ideal_1[:-1], srr_ideal_1, 'go-', label='ideal')
#srr_lsb = lsb_ideal_1[:aux]-usb_ideal_1[:aux]
#srr_usb = lsb_ideal_1[aux+1:]-usb_ideal_1[aux+1:]

#plt.plot(freq_ideal_1[:aux], srr_lsb, 'go-', label='ideal')
#plt.plot(freq_ideal_1[aux+1:], srr_usb, 'go-')

#calibrated
iters = 25
freq_cal_1 = np.arange(iters)+91.8

index = np.around((freq_cal_1-lo)/fs*fft_len)
index = np.abs(index).astype(int)

lsb_cal_1 = np.zeros(iters-1)
usb_cal_1 = np.zeros(iters-1)
for i in range(1,iters):
    d0_name = lo_dir+'test/'+str(i)+d0;
    d1_name = lo_dir+'test/'+str(i)+d1
    dout0 = np.loadtxt(d0_name, delimiter=',')
    dout1 = np.loadtxt(d1_name, delimiter=',')
    ind = index[i-1]
    #ind = np.argmax(dout0[:, 2])
    usb_cal_1[i-1] = 10*np.log10(dout0[ind,2]+1)
    lsb_cal_1[i-1] = 10*np.log10(dout1[ind,2]+1)

aux = len(freq_cal_1)/2
srr_cal_1 = np.abs(lsb_cal_1-usb_cal_1)
srr_cal_1 = np.hstack([srr_cal_1[:aux], srr_cal_1[aux+1:]])
freq_cal_1 = np.hstack([freq_cal_1[:aux], freq_cal_1[aux+1:]])
plt.plot(freq_cal_1[:-1], srr_cal_1, 'm*-', label='ideal')
#srr_lsb = lsb_cal_1[:aux]-usb_cal_1[:aux]
#srr_usb = lsb_cal_1[aux+1:]-usb_cal_1[aux+1:]
#plt.plot(freq_cal_1[:aux], srr_lsb, 'm*-', label='calibrated')
#plt.plot(freq_cal_1[aux+1:], srr_usb, 'm*-')

plt.grid()
plt.xlabel('GHz')
plt.ylabel('dB')
plt.title('SRR Test dataset')
plt.legend()
plt.show()
