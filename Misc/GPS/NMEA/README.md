# NMEA

This model receive NMEA data using the ROACH GPIOs via UART.
The system search for the $GPSZDA command and save the time related information. The subsecond time is taken from a PPS signal.

## Implementation info

This model uses some logic to program a ublox gps to output the GPSZDA command (the model was tested with the BG7TBL), then search for the pattern in the commands that the GPS is sending.
When a message with the time is received the module save the current time, the seconds field is update with a the PPS pulse. Also we keep track of the PPS with a counter that gets reset with every rising edge on the PPS.

For the ROACH2 caution must be take because the GPIOS are 1,5V tolerant so it could need a previous voltage translation.

The example model was compiled at 100MHz, if you want to use another clock frequency check that the CLK_FREQ parameter in the HDLs are set right.
#GPIO mapping

gpio0:  PPS
gpi01:  UART RX (connected with the TX of the GPS)
gpio2:  UART TX (connected with the RX of the GPS, is only used to program the ublox if its needed)


