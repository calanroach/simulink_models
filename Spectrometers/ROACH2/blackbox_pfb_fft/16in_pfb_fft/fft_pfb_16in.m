%Configure the pfb and wideband fft and produce the ngc files
fft_size = 10;
clock_mhz = 150; 

pfb_inwidth= 8;
pfb_outwidth = 18;      %this is also the fft output width

%delays
pfb_add_lat = 1;
pfb_mult_lat = 2;
pfb_bram_lat = 3;
pfb_fanout_lat = 2;
pfb_convert_lat = 1;

fft_add_lat = 1;
fft_mult_lat = 2;
fft_bram_lat = 2;
fft_input_lat = 2;
fft_convert_lat = 3;



model_name = 'pfb_fft_16in';

%input size
for i = [0:1:15]
   aux = strcat(model_name,'/dat',int2str(i));
   set_param(aux,'n_bits', int2str(pfb_inwidth));
   set_param(aux, 'bin_pt', int2str(pfb_inwidth-1));
end

%pfb parameters
set_param(strcat(model_name,'/pfb_fir_real'), 'PFBSize', int2str(fft_size));

set_param(strcat(model_name,'/pfb_fir_real'), 'BitWidthOut', int2str(pfb_outwidth));
set_param(strcat(model_name,'/pfb_fir_real'), 'BitWidthIn', int2str(pfb_inwidth));

set_param(strcat(model_name, '/pfb_fir_real'),'add_latency', int2str(pfb_add_lat));
set_param(strcat(model_name, '/pfb_fir_real'), 'mult_latency', int2str(pfb_mult_lat));
set_param(strcat(model_name, '/pfb_fir_real'), 'bram_latency', int2str(pfb_bram_lat));
set_param(strcat(model_name, '/pfb_fir_real'), 'fan_latency', int2str(pfb_fanout_lat));
set_param(strcat(model_name, '/pfb_fir_real'), 'conv_latency', int2str(pfb_convert_lat));

%set shift parameter
set_param(strcat(model_name, '/Constant20'), 'n_bits', int2str(fft_size));
set_param(strcat(model_name, '/Constant20'), 'const', int2str(2^(fft_size-1)-1));


set_param(strcat(model_name, '/fft_wideband_real'),'FFTSize', int2str(fft_size));
set_param(strcat(model_name, '/fft_wideband_real'),'input_bit_width', int2str(pfb_outwidth));
set_param(strcat(model_name, '/fft_wideband_real'),'bin_pt_in', int2str(pfb_outwidth-1));
set_param(strcat(model_name, '/fft_wideband_real'),'add_latency', int2str(fft_add_lat));
set_param(strcat(model_name, '/fft_wideband_real'),'mult_latency', int2str(fft_mult_lat));
set_param(strcat(model_name, '/fft_wideband_real'),'bram_latency', int2str(fft_bram_lat));
set_param(strcat(model_name, '/fft_wideband_real'),'conv_latency', int2str(fft_convert_lat));
set_param(strcat(model_name, '/fft_wideband_real'),'input_latency', int2str(fft_input_lat));

%set clock rate
set_param(strcat(model_name, '/XSG_core_config'), 'clk_rate', int2str(clock_mhz));

%setup the compilation 
%we need to uncheck the include clock wrapper
ngc_config.include_clockwrapper = 0;
ngc_config.include_cf = 0;

xsg_blk = strcat(model_name, '/ System Generator');

xlsetparam(xsg_blk ,'ngc_config', ngc_config);
%xlsetparam(xsg_blk ,'directory', './fft_pfb_8in');

%now start the compilation
disp('Running system generator ...');
xsg_result = xlGenerateButton(xsg_blk);
if xsg_result == 0,
    disp('XSG generation complete.');
else
    error(['XSG generation failed: ',xsg_result]);
end

%move the ngc generated 
copyfile pfb_fft_16in/sysgen/pfb_fft_16in.ngc pfb_fft_16in.ngc
copyfile pfb_fft_16in/sysgen/pfb_fft_16in.vhd pfb_fft_16in.vhd
extract_entity('./pfb_fft_16in.ngc')

%delete the sysgen folder 
rmdir pfb_fft_16in s
