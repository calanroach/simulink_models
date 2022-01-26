//`default_nettype none
//`include "irig_bcd.v"

module irig_time (
    input wire clk,
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



irig_bcd irig_bcd_inst
(
    .clk(clk),
    .rst(rst),
    .calibrate(calibrate),
    .cont(cont),
    .one_count(one_count),
    .zero_count(zero_count),
    .id_count(id_count),
    .debounce(debounce),
    .din(din),
    .sec(first_sec),
    .min(first_min),
    .hr(first_hr),
    .day(first_day),
    .bcd_valid(bcd_valid),
    .pps(pps),
    .irig_bit(irig_bit),
    .irig_bit_valid(irig_bit_valid),
    .state_out(state_out)
);


reg [5:0] sec_r=0, min_r=0;
reg [4:0] hr_r=0;
reg [8:0] day_r=0;
reg bcd_valid_r =0;

always@(posedge clk)begin
    bcd_valid_r <= bcd_valid;
    if(bcd_valid & ~bcd_valid_r)begin
        sec_r <= first_sec;
        min_r <= first_min;
        hr_r <= first_hr;
        day_r <= first_day;
    end
    else if(bcd_valid & pps)begin
        if(sec_r == 59)begin
            sec_r <=0;
            if(min_r ==59)begin
                min_r <=0;
                if(hr_r==23)begin
                    hr_r<=0;
                    if(day_r==364)
                        day_r <=0;
                    else
                        day_r <= day_r+1;
                end
                else
                    hr_r <=hr_r+1;
            end
            else
                min_r <= min_r+1;
        end
        else
            sec_r <= sec_r+1;
    end
end

assign sec = sec_r;
assign min = min_r;
assign hr = hr_r;
assign day = day_r;

//subsecond counter
reg [31:0] subsec_count=0;
always@(posedge clk)begin
    if(bcd_valid)begin
        if(pps)
           subsec_count<=0;
       else
           subsec_count <= subsec_count+1;
    end
    else 
        subsec_count <= 0;
end

assign subsec = subsec_count;

endmodule
