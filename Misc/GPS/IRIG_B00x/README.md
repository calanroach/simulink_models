# IRIG B00x

This model receive a DC IRIG-B0xx using the ROACH GPIOs.

The IRIG format consists in 100 pulses sent in 1 second. The duration of each pulse is translated to a 3 posible value: low, high and reference. The position of the pulse in the frame also encode the actual value.
Check [here](https://www.meinbergglobal.com/english/info/irig.htm) for more information about the format.

The model search for the BCD data in the frame, also there is a counter that keeps track for the subsecond inside the IRIG frame.

