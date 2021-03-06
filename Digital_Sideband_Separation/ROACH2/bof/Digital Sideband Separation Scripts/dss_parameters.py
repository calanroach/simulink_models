# File with all the basic parameters for multi LO scripts

# imports
import datetime, pyvisa
import numpy as np

# communication parameters
#roach_ip          = '133.40.220.2'
roach_ip          = None
boffile           = 'dss_2048ch_1520mhz.bof.gz'
rf_generator_name = "TCPIP::192.168.1.34::INSTR"
#rm = pyvisa.ResourceManager('@py')
rm = pyvisa.ResourceManager('@sim')

# model parameters
adc_bits           = 8
bandwidth          = 1080 # MHz
cal_acc_len_reg    = 'cal_acc_len'
syn_acc_len_reg    = 'syn_acc_len'
cnt_rst_reg        = 'cnt_rst'
bram_addr_width    = 8  # bits
bram_word_width    = 64 # bits
pow_data_type      = '>u8'
crosspow_data_type = '>i8'
consts_nbits       = 32
consts_binpt       = 27
bram_a2    = ['dout_a2_0', 'dout_a2_1', 'dout_a2_2', 'dout_a2_3', 
              'dout_a2_4', 'dout_a2_5', 'dout_a2_6', 'dout_a2_7']
bram_b2    = ['dout_b2_0', 'dout_b2_1', 'dout_b2_2', 'dout_b2_3', 
              'dout_b2_4', 'dout_b2_5', 'dout_b2_6', 'dout_b2_7']
bram_ab_re = ['dout_ab_re0', 'dout_ab_re1', 'dout_ab_re2', 'dout_ab_re3', 
              'dout_ab_re4', 'dout_ab_re5', 'dout_ab_re6', 'dout_ab_re7']
bram_ab_im = ['dout_ab_im0', 'dout_ab_im1', 'dout_ab_im2', 'dout_ab_im3', 
              'dout_ab_im4', 'dout_ab_im5', 'dout_ab_im6', 'dout_ab_im7']
bram_usb = ['dout0_0', 'dout0_1', 'dout0_2', 'dout0_3', 
            'dout0_4', 'dout0_5', 'dout0_6', 'dout0_7']
bram_lsb = ['dout1_0', 'dout1_1', 'dout1_2', 'dout1_3', 
            'dout1_4', 'dout1_5', 'dout1_6', 'dout1_7']
# constants where USB is maximized (LSB is rejected)
bram_consts_usb_re = ['bram_mult0_0_bram_re', 'bram_mult0_1_bram_re',
                      'bram_mult0_2_bram_re', 'bram_mult0_3_bram_re',
                      'bram_mult0_4_bram_re', 'bram_mult0_5_bram_re',
                      'bram_mult0_6_bram_re', 'bram_mult0_7_bram_re']
bram_consts_usb_im = ['bram_mult0_0_bram_im', 'bram_mult0_1_bram_im',
                      'bram_mult0_2_bram_im', 'bram_mult0_3_bram_im',
                      'bram_mult0_4_bram_im', 'bram_mult0_5_bram_im',
                      'bram_mult0_6_bram_im', 'bram_mult0_7_bram_im']
# constants where LSB is maximized (USB is rejected)
bram_consts_lsb_re = ['bram_mult1_0_bram_re', 'bram_mult1_1_bram_re',
                      'bram_mult1_2_bram_re', 'bram_mult1_3_bram_re',
                      'bram_mult1_4_bram_re', 'bram_mult1_5_bram_re',
                      'bram_mult1_6_bram_re', 'bram_mult1_7_bram_re']
bram_consts_lsb_im = ['bram_mult1_0_bram_im', 'bram_mult1_1_bram_im',
                      'bram_mult1_2_bram_im', 'bram_mult1_3_bram_im',
                      'bram_mult1_4_bram_im', 'bram_mult1_5_bram_im',
                      'bram_mult1_6_bram_im', 'bram_mult1_7_bram_im']

# experiment parameters
lo_freq     = 3 # GHz
rf_power    = 7 # dBm
acc_len     = 2**16
chnl_step   = 256
date_time   =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
cal_datadir = "dss_cal "     + date_time
srr_datadir = "dss_srr "     + date_time
pause_time  = 0.5 # should be > (1/bandwidth * FFT_size * acc_len * 2) in 
                      # order  for the spectra to be fully computed after a 
                      # tone change
load_consts = True
load_ideal  = False
caltar      = 'dss_cal 2020-03-21 22:20:25.tar.gz'

# derivative parameters
nchannels     = 2**bram_addr_width * len(bram_a2)
if_freqs      = np.linspace(0, bandwidth, nchannels, endpoint=False) # MHz
test_channels = range(1, nchannels, chnl_step)
if_test_freqs = if_freqs[test_channels] # MHz
rf_freqs_usb  = lo_freq + (if_freqs/1e3) # GHz
rf_freqs_lsb  = lo_freq - (if_freqs/1e3) # GHz
dBFS          = 6.02*adc_bits + 1.76 + 10*np.log10(nchannels)
