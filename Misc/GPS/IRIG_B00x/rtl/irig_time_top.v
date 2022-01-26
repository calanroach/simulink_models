
module irig_time_top (
    input wire clk,
    input wire ce,
    input wire rst,

    input wire calibrate,
    input wire cont, //if you want to be trying to calibrate always put this in 1
    input wire [31:0] one_count, zero_count, id_count,
    input wire [31:0] debounce,

    input wire din,
    
    //first bcd data
    output wire [5:0] first_sec,  
    output wire [5:0] first_min,
    output wire [4:0] first_hr,
    output wire [8:0] first_day,
    output wire bcd_valid,
    
    output wire [5:0] sec,  
    output wire [5:0] min,
    output wire [4:0] hr,
    output wire [8:0] day,

    output wire [31:0] subsec,
    //output pps each second
    output wire pps,

    //debug signals
    output wire [1:0] irig_bit,
    output wire irig_bit_valid,
    output wire [3:0] state_out
);


irig_time irig_time_inst (
    .clk(clk),
    .rst(rst),
    .calibrate(calibrate),
    .cont(cont),
    .one_count(one_count),
    .zero_count(zero_count),
    .id_count(id_count),
    .debounce(debounce),
    .din(din),
    .first_sec(first_sec),  
    .first_min(first_min),
    .first_hr(first_hr),
    .first_day(first_day),
    .bcd_valid(bcd_valid),
    .sec(sec),  
    .min(min),
    .hr(hr),
    .day(day),
    .subsec(subsec),
    .pps(pps),
    .irig_bit(irig_bit),
    .irig_bit_valid(irig_bit_valid),
    .state_out(state_out)
);


endmodule
