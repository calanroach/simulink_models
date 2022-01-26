%%function to obtain the adc input values
function [adc0, adc1, adc2,adc3,adc4,adc5,adc6,adc7,adc8,adc9,adc10,adc11,adc12,adc13,adc14,adc15] = adc_inputs(din)
    length = floor(size(din)/16);
    %t = [0:1:length-1];
    val0 = din(1:16:end);   val1 = din(2:16:end);   val2 = din(3:16:end);
    val3 = din(4:16:end);   val4 = din(5:16:end);   val5 = din(6:16:end);
    val6 = din(7:16:end);   val7 = din(8:16:end);   val8 = din(9:16:end);
    val9 = din(10:16:end);  val10 = din(11:16:end); val11 = din(12:16:end);
    val12 = din(13:16:end); val13 = din(14:16:end); val14 = din(15:16:end);
    val15 = din(16:16:end); 
    
    
    adc0.time=[]; adc1.time=[];adc2.time=[];adc3.time=[];adc4.time=[];
    adc5.time=[]; adc6.time=[];adc7.time=[];adc8.time=[];adc9.time=[];
    adc10.time=[]; adc11.time=[];adc12.time=[];adc13.time=[];adc14.time=[];
    adc15.time=[];
    adc0.signals.values = val0'; adc1.signals.values=val1';
    adc2.signals.values = val2'; adc3.signals.values=val3';
    adc4.signals.values = val4'; adc5.signals.values=val5';
    adc6.signals.values = val6'; adc7.signals.values=val7';
    adc8.signals.values = val8'; adc9.signals.values=val9';
    adc10.signals.values = val10'; adc11.signals.values=val11';
    adc12.signals.values = val12'; adc13.signals.values=val13';
    adc14.signals.values = val14'; adc15.signals.values=val15';
    
    adc0.signals.dimensions=1;  adc1.signals.dimensions=1;
    adc2.signals.dimensions=1;  adc3.signals.dimensions=1;
    adc4.signals.dimensions=1;  adc5.signals.dimensions=1;
    adc6.signals.dimensions=1;  adc7.signals.dimensions=1;
    adc8.signals.dimensions=1;  adc9.signals.dimensions=1;
    adc10.signals.dimensions=1;  adc11.signals.dimensions=1;
    adc12.signals.dimensions=1;  adc13.signals.dimensions=1;
    adc14.signals.dimensions=1;  adc15.signals.dimensions=1;
    
    
    %adc0 = timeseries(val0, t');     adc1 = timeseries(val1, t');
    %adc2 = timeseries(val2, t');     adc3 = timeseries(val3, t');
    %adc4 = timeseries(val4, t');     adc5 = timeseries(val5, t');
    %adc6 = timeseries(val6, t');     adc7 = timeseries(val7, t');
    %adc8 = timeseries(val8, t');     adc9 = timeseries(val9, t');
    %adc10 = timeseries(val10, t');   adc11 = timeseries(val11, t');
    %adc12 = timeseries(val12, t');   adc13 = timeseries(val13, t');
    %adc14 = timeseries(val14, t');   adc15 = timeseries(val15, t');
end
