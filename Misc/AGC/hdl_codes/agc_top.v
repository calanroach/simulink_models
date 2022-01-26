
module agc_top #(
    parameter DIN_WIDTH = 8,
    parameter DIN_POINT = 7,
    parameter PARALLEL = 8,
    parameter DELAY_LINE = 64,
    parameter UPDATE_CYCLES = 1024,
    parameter COEF_WIDTH = 16,
    parameter COEF_POINT = 8,
    parameter GAIN_WIDTH = 16,
    parameter GAIN_POINT = 8,
    parameter GAIN_HIGH = 2048, //in sd is 8
    parameter GAIN_LOW = 0
) (
    input wire clk,
    input wire ce,
    input wire rst,
    
    input wire [63:0] din,
    input wire din_valid,
    
    input wire [15:0] ref_pow,
    input wire [15:0] error_coef,
    
    output wire signed [15:0] gain_out,
    output wire gain_out_valid,

    output wire signed [191:0] dout,
    output wire dout_valid
);



agc #(
    .DIN_WIDTH(DIN_WIDTH),
    .DIN_POINT(DIN_POINT),
    .PARALLEL(PARALLEL),
    .DELAY_LINE(DELAY_LINE),
    .AVG_POW_APROX("nearest"),
    .UPDATE_CYCLES(UPDATE_CYCLES),
    .COEF_WIDTH(COEF_WIDTH),
    .COEF_POINT(COEF_POINT),
    .GAIN_WIDTH(GAIN_WIDTH),
    .GAIN_POINT(GAIN_POINT),
    .GAIN_HIGH(GAIN_HIGH),
    .GAIN_LOW(GAIN_LOW)
) agc_inst (
    .clk(clk),
    .rst(rst),
    .din(din),
    .din_valid(din_valid),
    .ref_pow(ref_pow),
    .error_coef(error_coef),
    .gain_out(gain_out),
    .gain_out_valid(gain_out_valid),
    .dout(dout),
    .dout_valid(dout_valid)
);
endmodule 
