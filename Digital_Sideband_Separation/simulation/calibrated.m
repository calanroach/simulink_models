dir = './data_david/';
sig_name1='Test_Data_IF_1_Filtered_RF_-35dBm_LO_8.8dBm_79.2GHz.txt';
sig_name2='Test_Data_IF_2_Filtered_RF_-35dBm_LO_8.8dBm_79.2GHz';

cal_dir = './cal/';

model_name = 'synthesis';
acc_len=5;
fft_len = 512;
sim_len = 1024;%2^15;

lsb_rom_head = 'rom_mult1_';
usb_rom_head = 'rom_mult0_';

model = load_system(model_name);

%calculate the weights for each rom
%2-24; 3-23; 4-22, etc.. 1 is alone :(
%13 is the clock
for i = [1:1:12]
    
    
end

const_w =  -1*ab_tonelsb/b2_tonelsb:        % ab*/ bb* = a/b
consts_lsb= -1*conj(ab_toneusb)/a2_toneusb  % (ab*)*/aa*=a*b/aa*=b/a