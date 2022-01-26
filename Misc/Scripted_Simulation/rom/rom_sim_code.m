% Here we want to modify the roms initial values via script
%hyperparameters
model_name = 'rom_sim';
block_name = 'ROM';
len = 1024;
seed = 10;

rng(seed);
rom_values = rand(1, len);
new_depth = log2(len);

%important parameters for a ROM, check xBlockHelp('ROM')
%depth          Int
%initVector     DoubleVector
%n_bits
%bin_pt

%to get the parameter of our ROM you could use get_param --> it returns str
rom_name = strcat(model_name, '/', block_name);
depth = str2num(get_param(rom_name, 'depth'));
init_vect = str2num(get_param(rom_name, 'initVector'));

fprintf('Old init vector[0] %i', init_vect(1));

%to set parameters in the rom 
aux_val = strcat('[', num2str(rom_values), ']');    %stupid matlab
set_param(rom_name, 'depth', int2str(len));
set_param(rom_name, 'initVector', aux_val);

%also need to set the bitwidth of the counter
set_param('rom_sim/Counter', 'n_bits', int2str(new_depth));

%set simulation
simulation = sim(model_name, 'StartTime','0','StopTime',int2str(len));

%get simultaion outputs
dout = simulation.get('simout').Data(:)';

%check if the output is what we expect
%avoid the first value (for the rom latency is not a valid value
dout = dout(2:end);                                     

error = dout-rom_values;
plot(error);
