
module mov_var_top (
    input wire clk,
	input wire ce,
    input wire rst,
    input wire [24:0] din,
    input wire din_valid,

    output wire signed [24:0] moving_avg,
    output wire signed [50:0] moving_var,
    output wire dout_valid
);


moving_var #(
    .DIN_WIDTH(25),
    .DIN_POINT(24),
    .WINDOW_LEN(128),
    .APROX("nearest")
) moving_var_inst (
    .clk(clk),
	.ce(ce),
    .rst(rst),
    .din(din),
    .din_valid(din_valid),
    .moving_avg(moving_avg),
    .moving_var(moving_var),
    .dout_valid(dout_valid)
);


endmodule 
