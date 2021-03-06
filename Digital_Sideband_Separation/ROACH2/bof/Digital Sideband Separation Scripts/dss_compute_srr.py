#!/usr/bin/python
# Script for SRR computation of digital sideband separating receiver. Computes 
# the Sideband Rejection Ratio by sweeping a tone through the bandwidth of a 
# calibrated model.
# It then saves the results into a compress folder.

# imports
import os, time, tarfile, shutil, json
import numpy as np
import matplotlib.pyplot as plt
import calandigital as cd
from dss_load_constants import dss_load_constants
from dss_parameters import *

def main():
    start_time = time.time()

    make_pre_measurements_actions()
    make_dss_measurements()
    make_post_measurements_actions()

    print("Finished. Total time: " + str(int(time.time() - start_time)) + "[s]")

def make_pre_measurements_actions():
    """
    Makes all the actions in preparation for the measurements:
    - initizalize ROACH and generator communications.
    - creating plotting and data saving elements
    - setting initial registers in FPGA
    - turning on generator power
    """
    global roach, rf_generator, fig, lines

    roach = cd.initialize_roach(roach_ip)
    rf_generator = rm.open_resource(rf_generator_name)

    print("Setting up plotting and data saving elements...")
    fig, lines = create_figure()
    make_data_directory()
    print("done")

    print("Setting accumulation register to " + str(acc_len) + "...")
    roach.write_int(syn_acc_len_reg, acc_len)
    print("done")
    print("Resseting counter registers...")
    roach.write_int(cnt_rst_reg, 1)
    roach.write_int(cnt_rst_reg, 0)
    print("done")

    print("Setting instruments power and outputs...")
    rf_generator.write("power " + str(rf_power))
    rf_generator.write("outp on")
    print("done")

def make_dss_measurements():
    """
    Makes the measurements for dss calibration.
    """
    # loading calibration constants
    if load_consts:
        dss_load_constants(roach, load_ideal, 0-1j, caltar)

    print("Starting tone sweep in upper sideband...")
    sweep_time = time.time()
    usb_toneusb, lsb_toneusb = get_srrdata(rf_freqs_usb, "usb")
    print("done (" +str(int(time.time() - sweep_time)) + "[s])")
        
    print("Starting tone sweep in lower sideband...")
    sweep_time = time.time()
    usb_tonelsb, lsb_tonelsb = get_srrdata(rf_freqs_lsb, "lsb")
    print("done (" +str(int(time.time() - sweep_time)) + "[s])")

    print("Saving data...")
    np.savez(srr_datadir+"/srrdata", 
        usb_toneusb=usb_toneusb, lsb_toneusb=lsb_toneusb,
        usb_tonelsb=usb_tonelsb, lsb_tonelsb=lsb_tonelsb)
    print("done")

    print("Printing data...")
    print_data()
    print("done")

def make_post_measurements_actions():
    """
    Makes all the actions required after measurements:
    - turn off sources
    - compress data
    """
    print("Turning off instruments...")
    rf_generator.write("outp off")
    rm.close()
    print("done")

    print("Compressing data...")
    compress_data(srr_datadir)
    print("done")

def create_figure():
    """
    Creates figure for plotting.
    """
    fig, [[ax0, ax1], [ax2, ax3]] = plt.subplots(2,2)
    fig.set_tight_layout(True)
    fig.show()
    fig.canvas.draw()
    
    # get line objects
    line0, = ax0.plot([],[])
    line1, = ax1.plot([],[])
    line2, = ax2.plot([],[])
    line3, = ax3.plot([],[])
    lines  = [line0, line1, line2, line3] 
    
    # set spectrometers axes
    ax0.set_xlim((0, bandwidth))     ; ax1.set_xlim((0, bandwidth))
    ax0.set_ylim((-85, 5))           ; ax1.set_ylim((-85, 5))
    ax0.grid()                       ; ax1.grid()
    ax0.set_xlabel('Frequency [MHz]'); ax1.set_xlabel('Frequency [MHz]')
    ax0.set_ylabel('Power [dBFS]')   ; ax1.set_ylabel('Power [dBFS]')
    ax0.set_title('USB spec')        ; ax1.set_title('LSB spec')

    # SRR axes
    ax2.set_xlim((0, bandwidth))     ; ax3.set_xlim((0, bandwidth))     
    ax2.set_ylim((0, 80))            ; ax3.set_ylim((0, 80))            
    ax2.grid()                       ; ax3.grid()                       
    ax2.set_xlabel('Frequency [MHz]'); ax3.set_xlabel('Frequency [MHz]')
    ax2.set_ylabel('SRR [dB]')       ; ax3.set_ylabel('SRR [dB]') 
    ax2.set_title('SRR USB')         ; ax3.set_title('SRR LSB')         

    return fig, lines

def make_data_directory():
    """
    Make directory where to save all the srr data.
    """
    os.mkdir(srr_datadir)

    # make .json file with test info
    testinfo = {}
    testinfo["roach ip"]          = roach_ip
    testinfo["date time"]         = date_time
    testinfo["boffile"]           = boffile
    testinfo["bandwidth mhz"]     = bandwidth
    testinfo["nchannels"]         = nchannels
    testinfo["acc len"]           = acc_len
    testinfo["chnl step"]         = chnl_step
    testinfo["lo freq ghz"]       = lo_freq
    testinfo["rf generator name"] = rf_generator_name
    testinfo["rf power dbm"]      = rf_power
    testinfo["load consts"]       = load_consts
    testinfo["load ideal"]        = load_ideal
    testinfo["caltar"]            = caltar

    with open(srr_datadir + "/testinfo.json", "w") as f:
        json.dump(testinfo, f, indent=4, sort_keys=True)

    # make rawdata folders
    os.mkdir(srr_datadir + "/rawdata_tone_usb")
    os.mkdir(srr_datadir + "/rawdata_tone_lsb")

def get_srrdata(rf_freqs, tone_sideband):
    """
    Sweep a tone through a sideband and get the srr data.
    The srr data is the power of each tone after applying the calibration
    constants for each sideband (usb and lsb).
    The full sprecta measured for each tone is saved to data for debugging
    purposes.
    :param rf_freqs: frequencies of the tones to perform the sweep (in GHz).
    :param tone_sideband: sideband of the injected test tone. Either USB or LSB
    :return: srr data: usb and lsb.
    """
    fig.canvas.set_window_title(tone_sideband.upper() + " Tone Sweep")

    usb_arr = []; lsb_arr = []
    for i, chnl in enumerate(test_channels):
        # set test tone
        freq = rf_freqs[chnl]
        rf_generator.ask("freq " + str(freq) + " ghz; *opc?")
        time.sleep(pause_time)

        # read data
        usb = cd.read_interleave_data(roach, bram_usb, bram_addr_width, 
                                      bram_word_width, pow_data_type)
        lsb = cd.read_interleave_data(roach, bram_lsb, bram_addr_width, 
                                      bram_word_width, pow_data_type)

        # append data to arrays
        usb_arr.append(usb[chnl])
        lsb_arr.append(lsb[chnl])

        # scale and dBFS data for plotting
        usb_plot = cd.scale_and_dBFS_specdata(usb, acc_len, dBFS)
        lsb_plot = cd.scale_and_dBFS_specdata(lsb, acc_len, dBFS)

        # compute srr for plotting
        if tone_sideband=='usb':
            srr = np.divide(usb_arr, lsb_arr)
        else: # tone_sideband=='lsb
            srr = np.divide(lsb_arr, usb_arr)

        # define sb plot line
        line_sb = lines[2] if tone_sideband=='usb' else lines[3]

        # plot data
        lines[0].set_data(if_freqs, usb_plot)
        lines[1].set_data(if_freqs, lsb_plot)
        line_sb.set_data(if_test_freqs[:i+1], 10*np.log10(srr))
        fig.canvas.draw()
        fig.canvas.flush_events()
        
        # save data
        np.savez(srr_datadir+"/rawdata_tone_" + tone_sideband + "/chnl_" + \
        str(chnl), usb=usb, lsb=lsb)

    # compute interpolations
    usb_arr = np.interp(if_freqs, if_test_freqs, usb_arr)
    lsb_arr = np.interp(if_freqs, if_test_freqs, lsb_arr)

    return usb_arr, lsb_arr

def print_data():
    """
    Print the saved data to .pdf images for an easy check.
    """
    # get data
    srrdata = np.load(srr_datadir + "/srrdata.npz")
    usb_toneusb = srrdata['usb_toneusb']; lsb_toneusb = srrdata['lsb_toneusb']
    usb_tonelsb = srrdata['usb_tonelsb']; lsb_tonelsb = srrdata['lsb_tonelsb']

    # compute SRR
    srr_usb = usb_toneusb / lsb_toneusb
    srr_lsb = lsb_tonelsb / usb_tonelsb

    # print SRR
    plt.figure()
    plt.plot(rf_freqs_usb, 10*np.log10(srr_usb), 'b')
    plt.plot(rf_freqs_lsb, 10*np.log10(srr_lsb), 'r')
    plt.grid()                 
    plt.xlabel('Frequency [GHz]')
    plt.ylabel('SRR [dB]')     
    plt.savefig(srr_datadir+'/srr.pdf')
    
def compress_data(datadir):
    """
    Compress the data from the datadir directory into a .tar.gz
    file and delete the original directory.
    :param datair: directory to compress.
    """
    tar = tarfile.open(datadir + ".tar.gz", "w:gz")
    for datafile in os.listdir(datadir):
        tar.add(datadir + '/' + datafile, datafile)
    tar.close()
    shutil.rmtree(datadir)

if __name__ == "__main__":
    main()
