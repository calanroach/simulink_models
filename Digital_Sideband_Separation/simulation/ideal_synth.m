%hyper params
dir = './data_david/';
name1='Test_Data_IF_1_Filtered_RF_-35dBm_LO_8.8dBm_79.2GHz.txt';
name2='Test_Data_IF_2_Filtered_RF_-35dBm_LO_8.8dBm_79.2GHz';

ideal_dir = './ideal/'

model_name = 'synthesis';
acc_len=5;
fft_len = 512;
sim_len = 1024;%2^15;


%
lsb_rom_head = 'rom_mult1_';
usb_rom_head = 'rom_mult0_';


model = load_system(model_name);
%closed it takes ~18 min
%open takes 

%load ideal constants
ideal_val = ones([fft_len/2,1])*(1j);
upload_weights(model_name,usb_rom_head, lsb_rom_head,ideal_val,ideal_val, 8);


%import the inpu data
path1=strcat(dir,name1);
path2=strcat(dir,name2);
dataIF1=importdata(path1);
dataIF2=importdata(path2);

Sampling_rate=24.5;   %%Gs/s 
time_step=1/(Sampling_rate*1e9);  %%Time step 1/Fs

din_data0 = zeros([1,sim_len+fft_len]);
din_data1 = zeros([1,sim_len+fft_len]);



for i=[1:1:n_data/2-1]
    tic
    data_sample_rate=1/(dataIF1.data(2,2*i-1)*1e-12); %%Get data sampling rate Hz/s
    first_NaN_index = find(isnan(dataIF1.data(:,2*i)), 1);
    clean_data_IF_1=dataIF1.data(1:first_NaN_index-1,2*i);
    Resampled_data_IF_1 = resample(clean_data_IF_1,round(Sampling_rate),round(data_sample_rate/(1e9)));
    clean_data_IF_2=dataIF2.data(1:first_NaN_index-1,2*i);  %%Removes all NaN data
    Resampled_data_IF_2 = resample(clean_data_IF_2,round(Sampling_rate),round(data_sample_rate/(1e9))); %%Resample at new rate
    
    %normalize the signals
    norm_value = max([max(Resampled_data_IF_1), max(Resampled_data_IF_2)]);
    sig0 = sig0/norm_value*0.9; %to no saturate the adc
    sig1 = sig1/norm_value*0.9;
    
    len_data = max(length(Resampled_data_IF_1), length(Resampled_data_IF_2));
    count = 0;
    count_word = sim_len+fft_len;
    while count_word>0
        din_data0(i,(count)*len_data+1:(count+1)*len_data) = Resampled_data_IF_1;
        din_data1(i,(count)*len_data+1:(count+1)*len_data) = Resampled_data_IF_2;
        count = count+1;
        count_word = count_word-len_data;
    end
    din_data0 = din_data0(1:sim_len);
    din_data1 = din_data1(1:sim_len);
   
    %create the input values
    [adc0_0,adc0_1,adc0_2,adc0_3,adc0_4,adc0_5,adc0_6,adc0_7, ...
    adc0_8,adc0_9,adc0_10,adc0_11,adc0_12,adc0_13,adc0_14,adc0_15] = adc_inputs(din_data0);

    [adc1_0,adc1_1,adc1_2,adc1_3,adc1_4,adc1_5,adc1_6,adc1_7, ...
    adc1_8,adc1_9,adc1_10,adc1_11,adc1_12,adc1_13,adc1_14,adc1_15] = adc_inputs(din_data1);

    %start simulation
    simulation = sim(model_name, 'StartTime','0','StopTime',int2str(sim_len-1));
    
    %read outputs
    
    dout0 = [];
    for i = [0:1:7]
        aux = strcat('dout0_',int2str(i));
        aux_pow = simulation.get(aux).Data(:);
        dout0 = [dout0, aux_pow];
    end

    dout1 = [];
    for i = [0:1:7]
        aux = strcat('dout1_',int2str(i));
        aux_pow = simulation.get(aux).Data(:);
        dout1 = [dout1, aux_pow];
    end

    dout0_ord = deinterleave_data(dout0,fft_len/2);
    dout1_ord = deinterleave_data(dout1,fft_len/2);
    
    
    %write the output into a file
    dout0_ord = double(dout0_ord);
    dout1_ord = double(dout1_ord);
    
    aux = strcat(ideal_dir, int2str(i));
    dlmwrite(strcat(aux, 'dout0.txt'), dout0_ord, 'precision', 32);
    dlmwrite(strcat(aux, 'dout1.txt'), dout1_ord, 'precision', 32);
    ex_time = toc;
    disp(['iter ',int2str(i) ,'takes ', num2str(ex_time/60.), ' minutes']) 
end


