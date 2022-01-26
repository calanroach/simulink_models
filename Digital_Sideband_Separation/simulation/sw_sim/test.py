import numpy as np
import matplotlib.pyplot as plt 
from scipy.fftpack import fft
import ipdb

#dat1 = np.loadtxt('SParam_Cal_Data_IF_1_ULTRA_Filtered_RF_-20dBm_LO_9dBm_79.2GHz.txt', skiprows=2)
#dat2 = np.loadtxt('SParam_Cal_Data_IF_2_ULTRA_Filtered_RF_-20dBm_LO_9dBm_79.2GHz.txt', skiprows=2)

dat1 = np.loadtxt('SParam_Cal_Data_IF_3_ULTRA_Filtered_RF_-20dBm_LO_9dBm_103.8GHz.txt', skiprows=2)
dat2 = np.loadtxt('SParam_Cal_Data_IF_4_ULTRA_Filtered_RF_-20dBm_LO_9dBm_103.8GHz.txt', skiprows=2)

freq1= dat1[:,0]; amp1=dat1[:,1]; phase1=dat1[:,2]
freq2= dat2[:,0]; amp2=dat2[:,1]; phase2=dat2[:,2]

amp_sig = 0.95*4
fft_len = 512
#freq_lo = 79.2
freq_lo = 103.8

freq1 = freq1-freq_lo
fs = 24.5
index = np.around(freq1/24.5*fft_len)
index = np.abs(index).astype(int)
#index = index[len(freq1)/2+1:].astype(int)

t = np.arange(fft_len)

#calibration part
a2 = np.zeros([fft_len/2,len(freq1)], dtype=complex)
b2 = np.zeros([fft_len/2,len(freq1)], dtype=complex)
ab = np.zeros([fft_len/2, len(freq1)], dtype=complex)

usb_const = np.ones(fft_len/2, dtype=complex)*0#1j
lsb_const = np.ones(fft_len/2, dtype=complex)*0#1j

for i in range(int(len(freq1))):
    sig1 = amp_sig*amp1[i]*np.sin(2*np.pi*freq1[i]/fs*t+np.deg2rad(phase1[i]))
    sig2 = amp_sig*amp2[i]*np.sin(2*np.pi*freq1[i]/fs*t+np.deg2rad(phase2[i]))
    spec1 = fft(sig1)
    spec2 = fft(sig2)
    a2[:,i] = spec1[:fft_len/2]*np.conj(spec1[:fft_len/2])
    b2[:,i] = spec2[:fft_len/2]*np.conj(spec2[:fft_len/2])
    ab[:,i] = spec1[:fft_len/2]*np.conj(spec2[:fft_len/2])
 
for j in range(int(len(freq1)/2)):
    ind = np.argmax(a2[:,j])
    ind2 = np.argmax(a2[:,len(freq1)-1-j])
    print("ind: %i %i"%(ind, ind2))
    a2_lsb = a2[ind,j]; 
    b2_lsb=b2[ind,j]; 
    ab_lsb=ab[ind,j]
    a2_usb = a2[ind,len(freq1)-1-j];
    b2_usb=b2[ind,len(freq1)-1-j]; 
    ab_usb=ab[ind,len(freq1)-1-j]
    usb_const[ind] = -1*ab_lsb/b2_lsb
    lsb_const[ind] = -1*np.conj(ab_usb)/a2_usb


#test data
#dat1 = np.loadtxt('SParam_Test_Data_IF_1_ULTRA_Filtered_RF_-35dBm_LO_8.8dBm_79.2GHz.txt',skiprows=2)
#dat2= np.loadtxt('SParam_Test_Data_IF_2_ULTRA_Filtered_RF_-35dBm_LO_8.8dBm_79.2GHz.txt',skiprows=2)


lsb_cal_data = np.zeros([fft_len/2, len(freq1)], dtype=complex)
usb_cal_data = np.zeros([fft_len/2, len(freq1)], dtype=complex)
usb_cal_data_max = np.zeros(len(freq1))
lsb_cal_data_max = np.zeros(len(freq1))


for i in range(len(freq1)):
    sig1 = amp_sig*amp1[i]*np.sin(2*np.pi*freq1[i]/fs*t+np.deg2rad(phase1[i]))
    sig2 = amp_sig*amp2[i]*np.sin(2*np.pi*freq1[i]/fs*t+np.deg2rad(phase2[i]))
    spec1 = fft(sig1)
    spec2 = fft(sig2)
    #ipdb.set_trace()
    usb_cal_data[:,i] = spec1[:fft_len/2]+usb_const*spec2[:fft_len/2]
    lsb_cal_data[:,i] = spec2[:fft_len/2]+lsb_const*spec1[:fft_len/2]
    usb_cal_data_max[i] = 20*np.log10(np.abs(usb_cal_data[index[i],i])+1)
    lsb_cal_data_max[i] = 20*np.log10(np.abs(lsb_cal_data[index[i],i])+1)









#dat1 = np.loadtxt('SParam_Test_Data_IF_1_ULTRA_Filtered_RF_-23dBm_LO_8.9dBm_79.2GHz.txt',skiprows=2)
#dat2 = np.loadtxt('SParam_Test_Data_IF_2_ULTRA_Filtered_RF_-23dBm_LO_8.9dBm_79.2GHz.txt',skiprows=2)

dat1 = np.loadtxt('SParam_Test_Data_IF_3_ULTRA_Filtered_RF_-23dBm_LO_8.9dBm_103.8GHz.txt',skiprows=2)
dat2 = np.loadtxt('SParam_Test_Data_IF_4_ULTRA_Filtered_RF_-23dBm_LO_8.9dBm_103.8GHz.txt',skiprows=2)

freq1= dat1[:,0]; amp1=dat1[:,1]; phase1=dat1[:,2]
freq2= dat2[:,0]; amp2=dat2[:,1]; phase2=dat2[:,2]

freq1 = freq1-freq_lo

spec_data1 = np.zeros([fft_len/2, len(freq1)], dtype=complex)
spec_data2 = np.zeros([fft_len/2, len(freq1)], dtype=complex)
lsb = np.zeros([fft_len/2, len(freq1)], dtype=complex)
usb = np.zeros([fft_len/2, len(freq1)], dtype=complex)
usb_max = np.zeros(len(freq1))
lsb_max = np.zeros(len(freq1))


lsb_cal = np.zeros([fft_len/2, len(freq1)], dtype=complex)
usb_cal = np.zeros([fft_len/2, len(freq1)], dtype=complex)
usb_cal_max = np.zeros(len(freq1))
lsb_cal_max = np.zeros(len(freq1))



for i in range(len(freq1)):
    sig1 = amp_sig*amp1[i]*np.sin(2*np.pi*freq1[i]/fs*t+np.deg2rad(phase1[i]))
    sig2 = amp_sig*amp2[i]*np.sin(2*np.pi*freq1[i]/fs*t+np.deg2rad(phase2[i]))
    spec1 = fft(sig1)
    spec2 = fft(sig2)
    spec_data1[:,i] = spec1[:fft_len/2]
    spec_data2[:,i] = spec2[:fft_len/2]
    usb[:,i] = spec1[:fft_len/2]+1j*spec2[:fft_len/2]
    lsb[:,i] = spec2[:fft_len/2]+1j*spec1[:fft_len/2]
    usb_max[i] = 20*np.log10(np.abs(usb[index[i],i])+1)
    lsb_max[i] = 20*np.log10(np.abs(lsb[index[i],i])+1)

    #ipdb.set_trace()
    usb_cal[:,i] = spec1[:fft_len/2]+usb_const*spec2[:fft_len/2]
    lsb_cal[:,i] = spec2[:fft_len/2]+lsb_const*spec1[:fft_len/2]
    usb_cal_max[i] = 20*np.log10(np.abs(usb_cal[index[i],i])+1)
    lsb_cal_max[i] = 20*np.log10(np.abs(lsb_cal[index[i],i])+1)




plt.figure()
plt.plot(freq2, usb_max,'*-',label='usb')
plt.plot(freq2, lsb_max,'*-',label='lsb' )
plt.xlabel('GHz')
plt.ylabel('dB')
plt.title('Ideal constants')
plt.ylim([-0.4,60])
plt.grid()
plt.legend()


plt.figure()
plt.plot(freq2, usb_cal_max,'*-', label='usb test data')
plt.plot(freq2, lsb_cal_max, '*-',label='lsb test data')
plt.plot(freq2, lsb_cal_data_max, '*-', label='lsb cal data')
plt.plot(freq2, usb_cal_data_max, '*-', label='usb cal data')
plt.xlabel('GHz')
plt.ylabel('dB')
plt.title('Calibrated constants')
plt.ylim([-0.4,60])
plt.grid()
plt.legend()

plt.figure()
srr_cal_lsb = lsb_cal_max[:len(freq1)/2]-usb_cal_max[:len(freq1)/2]
srr_cal_usb = usb_cal_max[len(freq1)/2+1:]-lsb_cal_max[len(freq1)/2+1:]

srr_lsb = lsb_max[:len(freq1)/2]-usb_max[:len(freq1)/2]
srr_usb = usb_max[len(freq1)/2+1:]-lsb_max[len(freq1)/2+1:]

srr_cal_data_lsb = lsb_cal_data_max[:len(freq1)/2]-usb_cal_data_max[:len(freq1)/2]
srr_cal_data_usb = usb_cal_data_max[len(freq1)/2+1:]-lsb_cal_data_max[len(freq1)/2+1:]

plt.plot(freq2[:len(freq1)/2],  srr_cal_lsb, 'r*-', label='calibrated (test data)')
plt.plot(freq2[len(freq1)/2+1:], srr_cal_usb, 'r*-')
plt.plot(freq2[:len(freq1)/2],  srr_lsb, 'b*-', label='ideal')
plt.plot(freq2[len(freq1)/2+1:], srr_usb, 'b*-')

plt.plot(freq2[:len(freq1)/2],  srr_cal_data_lsb, 'g*-', label='calibrated (cal data)')
plt.plot(freq2[len(freq1)/2+1:], srr_cal_data_usb, 'g*-')

plt.grid()
plt.legend()
plt.ylabel('SRR dB')
plt.xlabel('GHz')
plt.show()


