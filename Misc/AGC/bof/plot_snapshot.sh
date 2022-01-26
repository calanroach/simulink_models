#!/bin/bash
source configuration.sh
plot_snapshots.py \
    --ip         $(echo $ROACH_IP) \
    `#--bof      $(echo $BOF_FILE)` \
    --upload      \
    --snapnames  snapshot reduced \
    --dtype      ">b" \
    --nsamples   200
