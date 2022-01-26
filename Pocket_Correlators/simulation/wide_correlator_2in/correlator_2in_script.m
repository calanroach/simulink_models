%%hyper parameters
model_name = 'wide_correlator_2in';
acc_len=5;
fft_len = 4096;
sim_len = 1024*6;%2^15;

tic
%sim input data
frec = 780;
phase0 = 15;
phase1 = 40;
amp0 = 0.8;
amp1 = 0.5;
snr1 = 40;
snr2 = 20;


%generate input data
t = [0:1:fft_len-1];

sig1 = amp0*sin(2*pi*frec/fft_len*t+deg2rad(phase0));
sig2 = amp1*sin(2*pi*frec/fft_len*t+deg2rad(phase1));
sig1 = awgn(sig1,snr1);
sig2 = awgn(sig2,snr2);

%convert 
[adc0_0,adc0_1,adc0_2,adc0_3,adc0_4,adc0_5,adc0_6,adc0_7, ...
adc0_8,adc0_9,adc0_10,adc0_11,adc0_12,adc0_13,adc0_14,adc0_15] = adc_inputs(sig1);

[adc1_0,adc1_1,adc1_2,adc1_3,adc1_4,adc1_5,adc1_6,adc1_7, ...
adc1_8,adc1_9,adc1_10,adc1_11,adc1_12,adc1_13,adc1_14,adc1_15] = adc_inputs(sig2);

%set the accumulation len 
set_param(strcat(model_name, '/Constant'),'const', int2str(acc_len));


%Start simulation

simulation = sim(model_name, 'StartTime','0','StopTime',int2str(sim_len-1));
%set_param(model_name, 'SimulationCommand','start');


%pow0 = [powa_0.Data(:),powa_1.Data(:),powa_2.Data(:),powa_3.Data(:), ...
%       powa_4.Data(:),powa_5.Data(:),powa_6.Data(:),powa_7.Data(:)];
    
%pow1 = [powb_0.Data(:),powb_1.Data(:),powb_2.Data(:),powb_3.Data(:), ...
%        powb_4.Data(:),powb_5.Data(:),powb_6.Data(:),powb_7.Data(:)];

%corr_re = [corr_re0.Data(:),corr_re1.Data(:),corr_re2.Data(:),corr_re3.Data(:), ...
%           corr_re4.Data(:),corr_re5.Data(:),corr_re6.Data(:),corr_re7.Data(:)];
       
%corr_im = [corr_im0.Data(:),corr_im1.Data(:),corr_im2.Data(:),corr_im3.Data(:), ...
%           corr_im4.Data(:),corr_im5.Data(:),corr_im6.Data(:),corr_im7.Data(:)];
  
%get outputs, they should be of the same lenght.

pow0 = [];
for i = [0:1:7]
   aux = strcat('powa_',int2str(i));
   aux_pow = simulation.get(aux).Data(:);
   pow0 = [pow0, aux_pow];
end

pow1 = [];
for i = [0:1:7]
   aux = strcat('powb_',int2str(i));
   aux_pow = simulation.get(aux).Data(:);
   pow1 = [pow1, aux_pow];
end

corr_re = [];
for i = [0:1:7]
   aux = strcat('corr_re',int2str(i));
   aux_corr = simulation.get(aux).Data(:);
   corr_re = [corr_re, aux_corr];
end

corr_im = [];
for i = [0:1:7]
   aux = strcat('corr_im',int2str(i));
   aux_corr = simulation.get(aux).Data(:);
   corr_im = [corr_im, aux_corr];
end


%pow0_0 = simulation.get('pow0_0').Data(:)';
%pow0_1 = simulation.get('pow0_1').Data(:)';
%pow0_2 = simulation.get('pow0_2').Data(:)';
%pow0_3 = simulation.get('pow0_3').Data(:)';
%pow0_4 = simulation.get('pow0_4').Data(:)';
%pow0_5 = simulation.get('pow0_5').Data(:)';
%pow0_6 = simulation.get('pow0_6').Data(:)';
%pow0_7 = simulation.get('pow0_7').Data(:)';

%pow1_0 = simulation.get('pow1_0').Data(:)';
%pow1_1 = simulation.get('pow1_1').Data(:)';
%pow1_2 = simulation.get('pow1_2').Data(:)';
%pow1_3 = simulation.get('pow1_3').Data(:)';
%pow1_4 = simulation.get('pow1_4').Data(:)';
%pow1_5 = simulation.get('pow1_5').Data(:)';
%pow1_6 = simulation.get('pow1_6').Data(:)';
%pow1_7 = simulation.get('pow1_7').Data(:)';

%corr_re0 = simulaton.get('corr_re0').Data(:);
%corr_re1 = simulaton.get('corr_re1').Data(:);
%corr_re2 = simulaton.get('corr_re2').Data(:);
%corr_re3 = simulaton.get('corr_re3').Data(:);
%corr_re4 = simulaton.get('corr_re4').Data(:);
%corr_re5 = simulaton.get('corr_re5').Data(:);
%corr_re6 = simulaton.get('corr_re6').Data(:);
%corr_re7 = simulaton.get('corr_re7').Data(:);

%corr_im0 = simulaton.get('corr_im0').Data(:);
%corr_im1 = simulaton.get('corr_im1').Data(:);
%corr_im2 = simulaton.get('corr_im2').Data(:);
%corr_im3 = simulaton.get('corr_im3').Data(:);
%corr_im4 = simulaton.get('corr_im4').Data(:);
%corr_im5 = simulaton.get('corr_im5').Data(:);
%corr_im6 = simulaton.get('corr_im6').Data(:);
%corr_im7 = simulaton.get('corr_im7').Data(:);


%reorder the output data
pow0_data = deinterleave_data(pow0,fft_len/2);
pow1_data = deinterleave_data(pow1,fft_len/2);
corr_re_data = deinterleave_data(corr_re, fft_len/2);
corr_im_data = deinterleave_data(corr_im, fft_len/2);

corr_data = corr_re_data+1j*corr_im_data;
phase_data = rad2deg(angle(corr_data));

ex_time = toc;
disp(['one iter takes ', num2str(ex_time/60.), ' minutes'])