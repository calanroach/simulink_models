#!/bin/bash
plot_snapshots.py \
    --ip         192.168.0.40 \
    `#--bof      $(echo $BOF_FILE)` \
    --upload      \
    --snapnames  adcsnap0 adcsnap1\
    --dtype      ">b" \
    --nsamples   200
