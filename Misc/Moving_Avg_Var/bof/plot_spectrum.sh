#!/bin/bash
source configuration.sh

##this function is for look at the spectra when the system is programed
##<<Block_comment
./plot_spectrum.py \
    --ip        $(echo $ROACH_IP) \
    `#--bof       $(echo $BOF_FILE) `\
    --upload     \
    --bramnames spec1_0 spec1_1 spec1_2 spec1_3 \
    --nspecs    1 \
    --addrwidth 9 \
    --datawidth 64 \
    --bandwidth 600 \
    --nbits     8 
##Block_comment

##this one program it and shows you the spectrum, but it doesnt put the fft gain

<<Block_comment 
plot_spectra.py \
    --ip        $(echo $ROACH_IP) \
    --bof       $(echo $BOF_FILE) \ 
    --upload    \
    --bramnames dout0_0 dout0_1 dout0_2 dout0_3 \
                dout0_4 dout0_5 dout0_6 dout0_7 \
    --nspecs    1 \
    --addrwidth 11 \
    --datawidth 64 \
    --bandwidth 1080 \
    --nbits     8 \
    --countreg  cnt_rst \  
    --accreg    acc_len \
    --acclen    $(echo ACC_LEN)
Block_comment
