import numpy as np
import matplotlib.pyplot as plt 
from scipy.fftpack import fft
import matplotlib.lines as mlines
import ipdb

def calibrate_weights(cal1_data, cal2_data, lo_freq, amp_sig,fft_len, fs, adc_bits,
        const_bits):
    """ cal_data = [freq, amp1, phase]
        amp_sig = amplitude of the sine wave
    """
    freq = cal1_data[:,0]-lo_freq
    amp1 = cal1_data[:,1];  amp2 = cal2_data[:,1]
    phase1 = cal1_data[:,2];phase2=cal2_data[:,2] 
    index = np.around(freq/fs*fft_len)
    index = np.abs(index).astype(int)
    t = np.arange(fft_len)
    a2 = np.zeros([fft_len/2,len(freq)], dtype=complex)
    b2 = np.zeros([fft_len/2,len(freq)], dtype=complex)
    ab = np.zeros([fft_len/2, len(freq)], dtype=complex)
    usb_const = np.ones(fft_len/2, dtype=complex)*1j
    lsb_const = np.ones(fft_len/2, dtype=complex)*1j
    for i in range(len(freq)):
        sig1 = amp_sig*amp1[i]*np.sin(2*np.pi*freq[i]/fs*t+np.deg2rad(phase1[i]))
        sig2 = amp_sig*amp2[i]*np.sin(2*np.pi*freq[i]/fs*t+np.deg2rad(phase2[i]))
        #ipdb.set_trace()
        #discretize the input signal
        sig1 = ((sig1*2**adc_bits).astype(int))
        sig1 = sig1/(2.**adc_bits)
        sig2 = ((sig2*2**adc_bits).astype(int))
        sig2 = sig2/(2.**adc_bits)
        spec1 = fft(sig1)
        spec2 = fft(sig2)
        a2[:,i] = spec1[:fft_len/2]*np.conj(spec1[:fft_len/2])
        b2[:,i] = spec2[:fft_len/2]*np.conj(spec2[:fft_len/2])
        ab[:,i] = spec1[:fft_len/2]*np.conj(spec2[:fft_len/2])
    for j in range(int(len(freq)/2)):
        ind = np.argmax(a2[:,j])
        a2_lsb = a2[ind,j];
        b2_lsb=b2[ind,j];
        ab_lsb=ab[ind,j]
        a2_usb = a2[ind,len(freq)-1-j];
        b2_usb=b2[ind,len(freq)-1-j];
        ab_usb=ab[ind,len(freq)-1-j]
        usb_const[ind] = -1*ab_lsb/b2_lsb
        lsb_const[ind] = -1*np.conj(ab_usb)/a2_usb
    usb_const_re = (usb_const.real*2**const_bits).astype(int)
    usb_const_re = usb_const_re/(2.**const_bits)
    usb_const_im = (usb_const.imag*2**const_bits).astype(int)
    usb_const_im = usb_const_im/(2.**const_bits)
    usb_const = usb_const_re+1j*usb_const_im
    lsb_const_re = (lsb_const.real*2**const_bits).astype(int)
    lsb_const_re = lsb_const_re/(2.**const_bits)
    lsb_const_im = (lsb_const.imag*2**const_bits).astype(int)
    lsb_const_im = lsb_const_im/(2.**const_bits)
    lsb_const = lsb_const_re+1j*lsb_const_im
    return [usb_const, lsb_const]


def evaluate_data(test1_data, test2_data, usb_w,lsb_w, lo_freq,amp_sig,fft_len,fs, adc_bits):
    """idem as calibrate weights..
        usb_w, lsb_w = weights of the calibrated signal (ideal ones are 0+j)
    """
    freq = test1_data[:,0]-lo_freq
    amp1 = test1_data[:,1];  amp2 = test2_data[:,1]
    phase1 = test1_data[:,2];phase2=test2_data[:,2] 
    index = np.around(freq/fs*fft_len)
    index = np.abs(index).astype(int)
    t = np.arange(fft_len)
    usb_data = np.zeros(len(freq))
    lsb_data = np.zeros(len(freq))
    for i in range(len(freq)):
        sig1 = amp_sig*amp1[i]*np.sin(2*np.pi*freq[i]/fs*t+np.deg2rad(phase1[i]))
        sig2 = amp_sig*amp2[i]*np.sin(2*np.pi*freq[i]/fs*t+np.deg2rad(phase2[i]))
        #discretize the input signal
        #ipdb.set_trace()
        sig1 = ((sig1*2**adc_bits).astype(int))
        sig1 = sig1/(2.**adc_bits)
        sig2 = ((sig2*2**adc_bits).astype(int))
        sig2 = sig2/(2.**adc_bits)
        spec1 = fft(sig1)
        spec2 = fft(sig2)
        usb = spec1[:fft_len/2]+usb_w*spec2[:fft_len/2]
        lsb = spec2[:fft_len/2]+lsb_w*spec1[:fft_len/2]
        usb_data[i] = 20*np.log10(np.abs(usb[index[i]])+1)
        lsb_data[i] = 20*np.log10(np.abs(lsb[index[i]])+1)
    srr_lsb = lsb_data[:len(freq)/2]-usb_data[:len(freq)/2]
    srr_usb = usb_data[len(freq)/2+1:]-lsb_data[len(freq)/2+1:]
    return [usb_data, lsb_data, srr_lsb, srr_usb]




#lo 79.2
cal1 = np.loadtxt('SParam_Cal_Data_IF_1_ULTRA_Filtered_RF_-20dBm_LO_9dBm_79.2GHz.txt', skiprows=2)
cal2 = np.loadtxt('SParam_Cal_Data_IF_2_ULTRA_Filtered_RF_-20dBm_LO_9dBm_79.2GHz.txt', skiprows=2)

test1 = np.loadtxt('SParam_Test_Data_IF_1_ULTRA_Filtered_RF_-23dBm_LO_8.9dBm_79.2GHz.txt', skiprows=2)
test2 = np.loadtxt('SParam_Test_Data_IF_2_ULTRA_Filtered_RF_-23dBm_LO_8.9dBm_79.2GHz.txt', skiprows=2)

#lo 103.8
cal3 = np.loadtxt('SParam_Cal_Data_IF_3_ULTRA_Filtered_RF_-20dBm_LO_9dBm_103.8GHz.txt', skiprows=2)
cal4 = np.loadtxt('SParam_Cal_Data_IF_4_ULTRA_Filtered_RF_-20dBm_LO_9dBm_103.8GHz.txt', skiprows=2)

test3 = np.loadtxt('SParam_Test_Data_IF_3_ULTRA_Filtered_RF_-23dBm_LO_8.9dBm_103.8GHz.txt', skiprows=2)
test4 = np.loadtxt('SParam_Test_Data_IF_4_ULTRA_Filtered_RF_-23dBm_LO_8.9dBm_103.8GHz.txt', skiprows=2)

adc_bits = 8
const_bits = 32
fs = 24.5
amp_sig = 4.5
fft_size = 512

ideal_w = np.ones(fft_size/2)*1j

#first lo
lo = 79.2
usb_w, lsb_w = calibrate_weights(cal1,cal2,lo,amp_sig, fft_size,fs,adc_bits, const_bits)
#ideal weigths over the 

cal_usb_ideal, cal_lsb_ideal, cal_srr_lsb_ideal, cal_srr_usb_ideal = evaluate_data(cal1,cal2,
        ideal_w,ideal_w, lo, amp_sig, fft_size,fs, adc_bits)

cal_usb, cal_lsb, cal_srr_lsb, cal_srr_usb = evaluate_data(cal1,cal2,usb_w,
            lsb_w, lo, amp_sig, fft_size,fs, adc_bits)

test_usb, test_lsb, test_srr_lsb, test_srr_usb = evaluate_data(test1,test2,
        usb_w,lsb_w, lo, amp_sig, fft_size,fs, adc_bits)

test_usb_ideal, test_lsb_ideal, test_srr_lsb_ideal, test_srr_usb_ideal = evaluate_data(test1,
            test2,ideal_w,ideal_w, lo, amp_sig, fft_size,fs, adc_bits)

bands_lo0 = [cal_lsb, cal_usb, cal_lsb_ideal, cal_usb_ideal, test_lsb, 
            test_usb, test_lsb_ideal, test_usb_ideal]

srr_lo0 = [cal_srr_lsb, cal_srr_usb, cal_srr_lsb_ideal, cal_srr_usb_ideal, 
          test_srr_lsb, test_srr_usb, test_srr_lsb_ideal, test_srr_usb_ideal]
freq_lo0 = cal1[:,0]
freq_srr_lo0 = [freq_lo0[:len(freq_lo0)/2], freq_lo0[len(freq_lo0)/2+1:]]

#second lo
lo = 103.8
usb_w, lsb_w = calibrate_weights(cal3,cal4, lo,amp_sig, fft_size,fs, adc_bits, const_bits)
#ideal weigths over the 

cal_usb_ideal, cal_lsb_ideal, cal_srr_lsb_ideal, cal_srr_usb_ideal = evaluate_data(cal3,
        cal4,ideal_w,ideal_w, lo, amp_sig, fft_size,fs, adc_bits)

cal_usb, cal_lsb, cal_srr_lsb, cal_srr_usb = evaluate_data(cal3,cal4,usb_w,
        lsb_w, lo, amp_sig, fft_size,fs, adc_bits)

test_usb, test_lsb, test_srr_lsb, test_srr_usb = evaluate_data(test3,test4,
        usb_w,lsb_w, lo, amp_sig, fft_size,fs, adc_bits)

test_usb_ideal, test_lsb_ideal, test_srr_lsb_ideal, test_srr_usb_ideal = evaluate_data(test3,
        test4,ideal_w,ideal_w, lo, amp_sig, fft_size,fs, adc_bits)

bands_lo1 = [cal_lsb, cal_usb, cal_lsb_ideal, cal_usb_ideal, test_lsb, 
            test_usb, test_lsb_ideal, test_usb_ideal]

srr_lo1 = [cal_srr_lsb, cal_srr_usb, cal_srr_lsb_ideal, cal_srr_usb_ideal, 
          test_srr_lsb, test_srr_usb, test_srr_lsb_ideal, test_srr_usb_ideal]

freq_lo1 = cal4[:,0]
freq_srr_lo1 = [freq_lo1[:len(freq_lo1)/2], freq_lo1[len(freq_lo1)/2+1:]]



#figures

plt.title('Calibration Dataset')
plt.plot(freq_lo0, bands_lo0[0], 'r*-', label='calibrated')
plt.plot(freq_lo0, bands_lo0[1], 'r*-')
plt.plot(freq_lo0, bands_lo0[2], 'bo-', label='ideal')
plt.plot(freq_lo0, bands_lo0[3], 'bo-')

plt.plot(freq_lo1, bands_lo1[0], 'm*-', label='calibrated')
plt.plot(freq_lo1, bands_lo1[1], 'm*-')
plt.plot(freq_lo1, bands_lo1[2], 'go-', label='ideal')
plt.plot(freq_lo1, bands_lo1[3], 'go-')

plt.legend()
plt.grid()
plt.ylabel('dB')
plt.xlabel('GHz')

plt.figure()
plt.title('SRR Calibration Dataset')
plt.plot(freq_srr_lo0[0], srr_lo0[0], 'r*-', label='calibrated')
plt.plot(freq_srr_lo0[1], srr_lo0[1], 'r*-')
plt.plot(freq_srr_lo0[0], srr_lo0[2], 'bo-', label='ideal')
plt.plot(freq_srr_lo0[1], srr_lo0[3], 'bo-')

plt.plot(freq_srr_lo1[0], srr_lo1[0], 'm*-', label='calibrated')
plt.plot(freq_srr_lo1[1], srr_lo1[1], 'm*-')
plt.plot(freq_srr_lo1[0], srr_lo1[2], 'go-', label='ideal')
plt.plot(freq_srr_lo1[1], srr_lo1[3], 'go-')

plt.legend()
plt.grid()
plt.ylabel('SRR dB')
plt.xlabel('GHz')

fig = plt.figure()
plt.title('Test Dataset')
plt.plot(freq_lo0, bands_lo0[4], 'r*-', label='calibrated')
plt.plot(freq_lo0, bands_lo0[5], 'r*-')
plt.plot(freq_lo0, bands_lo0[6], 'bo-', label='ideal')
plt.plot(freq_lo0, bands_lo0[7], 'bo-')


plt.plot(freq_lo1, bands_lo1[4], 'm*-', label='calibrated')
plt.plot(freq_lo1, bands_lo1[5], 'm*-')
plt.plot(freq_lo1, bands_lo1[6], 'go-', label='ideal')
plt.plot(freq_lo1, bands_lo1[7], 'go-')

plt.legend()
plt.grid()
plt.ylabel('dB')
plt.xlabel('GHz')


plt.figure()
plt.title('SRR Test Dataset')
plt.plot(freq_srr_lo0[0], srr_lo0[4], 'r*-', label='calibrated')
plt.plot(freq_srr_lo0[1], srr_lo0[5], 'r*-')
plt.plot(freq_srr_lo0[0], srr_lo0[6], 'bo-', label='ideal')
plt.plot(freq_srr_lo0[1], srr_lo0[7], 'bo-')

plt.plot(freq_srr_lo1[0], srr_lo1[4], 'm*-', label='calibrated')
plt.plot(freq_srr_lo1[1], srr_lo1[5], 'm*-')
plt.plot(freq_srr_lo1[0], srr_lo1[6], 'go-', label='ideal')
plt.plot(freq_srr_lo1[1], srr_lo1[7], 'go-')

plt.legend()
plt.grid()
plt.ylabel('SRR dB')
plt.xlabel('GHz')

plt.show()




adc_bits_test = [2,4,6,8,10]
cal_colors =   ['r*-','b*-','m*-','g*-','k*-','y*-','c*-']
ideal_colors = ['ro-','bo-','mo-','go-','ko-','yo-','co-']
for i in range(len(adc_bits_test)):
    lo = 79.2
    usb_w, lsb_w = calibrate_weights(cal1,cal2,lo,amp_sig, fft_size,fs,adc_bits_test[i], const_bits)
    test_usb, test_lsb, test_srr_lsb, test_srr_usb = evaluate_data(test1,test2,
            usb_w,lsb_w, lo, amp_sig, fft_size,fs, adc_bits_test[i])
    test_usb_ideal, test_lsb_ideal, test_srr_lsb_ideal, test_srr_usb_ideal = evaluate_data(test1,
            test2,ideal_w,ideal_w, lo, amp_sig, fft_size,fs, adc_bits_test[i])
    plt.plot(freq_srr_lo0[0], test_srr_lsb,cal_colors[i], label=str(adc_bits_test[i]))
    plt.plot(freq_srr_lo0[1], test_srr_usb, cal_colors[i])
    plt.plot(freq_srr_lo0[0], test_srr_lsb_ideal, ideal_colors[i])
    plt.plot(freq_srr_lo0[1], test_srr_usb_ideal, ideal_colors[i])

    lo = 103.8
    usb_w, lsb_w = calibrate_weights(cal3,cal4,lo,amp_sig, fft_size,fs,adc_bits_test[i], const_bits)
    test_usb, test_lsb, test_srr_lsb, test_srr_usb = evaluate_data(test3,test4,
            usb_w,lsb_w, lo, amp_sig, fft_size,fs, adc_bits_test[i])
    test_usb_ideal, test_lsb_ideal, test_srr_lsb_ideal, test_srr_usb_ideal = evaluate_data(test3,
            test4,ideal_w,ideal_w, lo, amp_sig, fft_size,fs, adc_bits_test[i])
    plt.plot(freq_srr_lo1[0], test_srr_lsb,cal_colors[i] )
    plt.plot(freq_srr_lo1[1], test_srr_usb, cal_colors[i])
    plt.plot(freq_srr_lo1[0], test_srr_lsb_ideal, ideal_colors[i])
    plt.plot(freq_srr_lo1[1], test_srr_usb_ideal, ideal_colors[i])

plt.legend()
plt.grid()
plt.show()


