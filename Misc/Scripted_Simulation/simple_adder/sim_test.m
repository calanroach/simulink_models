%test to how to automatize simulations in simulink (puaj, if you can avoid
%it use cocotb for you own mental sanity)

%hyperparameter
len = 1024;
model_name = 'test_sim';
seed = 10;

%test
model = load_system(model_name);


%input values
rng(seed);           %set the random seed
din = rand(2, len); %(inputs, len_test)
gold = din(1,:)+din(2,:);

t = [0:1:len-1];

%input port names 
%dat0 = timeseries(din(1,:), t');
%dat1 = timeseries(din(2,:), t');

dat0.signals.values = din(1,:)';
dat0.signals.dimensions =1;
dat0.time = [];
dat1.signals.values = din(2,:)';
dat1.signals.dimensions = 1;
dat1.time= [];

%SimOut = sim('MODEL', 'ReturnWorkspaceOutputs', 'on')
%simulation = sim(model_name, 'StartTime','0','StopTime',int2str(len-1));
simulation = sim(model_name,'StartTime','0','StopTime',int2str(len-1));

%get simultaion outputs
dout = simulation.get('simout').Data(:)';

%check the error of fixed point arithm
error = abs(dout-gold);

%plot the error
plot(error);
