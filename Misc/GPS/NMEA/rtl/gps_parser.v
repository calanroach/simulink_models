`default_nettype none
`define __GOLD_INIT__

module gps_parser #(
    parameter CLK_FREQ = 100_000_000,
    parameter BAUD_RATE = 9600,
    parameter MSG_LEN = 29, //to program the ublox gps
    parameter PATTERN_SIZE = 6, //$GPZDA,
    parameter INFO_SIZE = 22,   //hhmmss.ss,dd,mm,yyyy
    parameter MEM_FILE = "gold_hex.mem"
) (
    input wire clk,
    input wire ce,
    input wire rst,  //rst
    input wire program_ublox,  //program ublox
    input wire read_time,  //read the hour
    
    //outputs to simulink  
    output wire [5:0] data_index,
    output wire valid_data,
    output wire [7:0] time_data, 
    output wire led_out,

//    output wire o_UART_TX,
//    input wire i_UART_RX,

    input wire ublox_rx,   //rx ie goes with the rx of the gps
    output wire ublox_tx

);

    //program ublox
    reg [7:0] msg [28:0];
    initial begin
        $readmemh("gpszda.mem", msg);
    end
    
    
    wire [7:0] gps_tx_data;
    wire gps_tx_tvalid, gps_tx_tready;
    wire [$clog2(MSG_LEN)-1:0] msg_index;
    reg [7:0] msg_gps_tx=0;
    
    always@(posedge clk)begin
        msg_gps_tx <= msg[msg_index];
    end

    send_msg #(
        .MSG_LEN(MSG_LEN),
        .N_BITS(8)
    ) program_gps (
        .clk(clk),
        .rst(rst),
        .start_trans(program_ublox),
        .uart_tdata(gps_tx_data),
        .uart_tvalid(gps_tx_tvalid),
        .uart_tready(gps_tx_tready),
        .msg(msg_gps_tx),
        .msg_index(msg_index)
    );
    
    uart_tx #(
        .CLK_FREQ(CLK_FREQ),
        .BAUD_RATE(BAUD_RATE)
    ) gps_uart_tx (
        .axis_tdata(gps_tx_data),
        .axis_tvalid(gps_tx_tvalid),
        .axis_tready(gps_tx_tready),
        .clk(clk),
        .tx_data(ublox_tx)
    );

    //read the gps data and search the pattern
    

    wire [7:0]  gps_rx_data;
    wire gps_rx_tvalid, gps_rx_tready;
    assign gps_rx_tready = gps_rx_tvalid; 
    uart_rx #(
        .CLK_FREQ(CLK_FREQ),
        .BAUD_RATE(BAUD_RATE),
        .N_BITS(8)
    ) gps_rx_inst (
        .clk(clk),
        .rst(rst),
        .rx_data(ublox_rx),
        .uart_rx_tdata(gps_rx_data),    
        .uart_rx_tready(gps_rx_tready),
        .uart_rx_tvalid(gps_rx_tvalid)
    );

    reg r_valid_msg = 0;
    always@(posedge clk)begin
        r_valid_msg <= gps_rx_tvalid;
    end
    wire char_valid;
    assign char_valid = gps_rx_tvalid & ~r_valid_msg;  //rising edge detector
    wire [7:0] char_in;
    assign char_in = gps_rx_data;

    wire [7:0] zda_data;
    wire zda_valid;

    pattern_search #(
        .N_BITS(8),
        .PATTERN_SIZE(PATTERN_SIZE),
        .INFO_SIZE(INFO_SIZE),
        .MEM_FILE(MEM_FILE)
    ) pattern_search_inst (
        .clk(clk),
        .rst(rst),
        .char_in(char_in),
        .char_valid(char_valid),
        .golden_word(),
        .golden_word_valid(1'b0),
        .golden_word_index(),
        .info_data(zda_data),
        .info_valid(zda_valid)
    );

    reg [7:0] zda_time [INFO_SIZE-1:0];
    reg [$clog2(INFO_SIZE)-1:0] time_ind=0;

/*    
    always@(posedge clk)begin
        if(rst)begin
            time_ind <= 0;
        end
        else begin
            if(zda_valid)begin
                if(time_ind <(INFO_SIZE-1))begin
                    zda_time[time_ind] <= zda_data;
                    time_ind <=time_ind +1;
                end
                else begin
                    time_ind <= time_ind;
                end
            end
        end
    end
  */

    always@(posedge clk)begin
        if(rst)begin
            time_ind <= 0;
        end
        else begin
            if(zda_valid)begin
                if(time_ind <(INFO_SIZE-1))begin
                    zda_time[time_ind] <= zda_data;
                    time_ind <=time_ind +1;
                end
                else begin
                    time_ind <= time_ind;
                end
            end
        end
    end

    assign valid_data = zda_valid;
    assign data_index = time_ind;
    assign time_data = zda_data;

    //finish the calibration
    assign led_out = ~(time_ind <(INFO_SIZE-1));

    //send the data to the uart;
    /*
    wire [7:0] fpga_tx_data;
    wire fpga_tx_tvalid, fpga_tx_tready;
    wire [$clog2(MSG_LEN)-1:0] fpga_index;
    reg [7:0] msg_fpga_tx=0;
    
    always@(posedge clk)begin
        msg_fpga_tx <= zda_time[fpga_index];
    end

    send_msg #(
        .MSG_LEN(MSG_LEN),
        .N_BITS(8)
    ) send_fpga (
        .clk(clk),
        .rst(rst),
        .start_trans(read_time),
        .uart_tdata(fpga_tx_data),
        .uart_tvalid(fpga_tx_tvalid),
        .uart_tready(fpga_tx_tready),
        .msg(msg_fpga_tx),
        .msg_index(fpga_index)
    );
    
    uart_tx #(
        .CLK_FREQ(CLK_FREQ),
        .BAUD_RATE(BAUD_RATE)
    ) fpga_uart_tx (
        .axis_tdata(fpga_tx_data),
        .axis_tvalid(fpga_tx_tvalid),
        .axis_tready(fpga_tx_tready),
        .clk(clk),
        .tx_data(o_UART_TX)
    );

    //the message we receive is 
    //,210935.00,13,11,2020
    // to be done... always have that size??
    
    */


endmodule 

