#!/usr/bin/env python2
import argparse
import calandigital as cd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

parser = argparse.ArgumentParser(
    description="Plot spectra from an spectrometer model in ROACH.")
parser.add_argument("-i", "--ip", dest="ip", default=None,
    help="ROACH IP address.")
parser.add_argument("-b", "--bof", dest="boffile",
    help="Boffile to load into the FPGA.")
parser.add_argument("-u", "--upload", dest="upload", action="store_true",
    help="If used, upload .bof from PC memory (ROACH2 only).")
parser.add_argument("-bn", "--bramnames", dest="bramnames", nargs="*",
    help="Names of bram blocks to read.")
parser.add_argument("-ns", "--nspecs", dest="nspecs", type=int, default=2,
    choices={1,2,4,16}, help="Number of independent spectra to plot.")
parser.add_argument("-aw", "--addrwidth", dest="awidth", type=int, default=9,
    help="Width of bram address in bits.")
parser.add_argument("-dw", "--datawidth", dest="dwidth", type=int, default=64,
    help="Width of bram data in bits.")
parser.add_argument("-bw", "--bandwidth", dest="bandwidth", type=float, default=1080,
    help="Bandwidth of the spectra to plot in MHz.")
parser.add_argument("-nb", "--nbits", dest="nbits", type=int, default=8,
    help="Number of bits used to sample the data (ADC bits).")
parser.add_argument("-cr", "--countreg", dest="count_reg", default="cnt_rst",
    help="Counter register name. Reset at initialization.")
parser.add_argument("-ar", "--accreg", dest="acc_reg", default="acc_len",
    help="Accumulation register name. Set at initialization.")
parser.add_argument("-al", "--acclen", dest="acclen", type=int, default=2**16,
    help="Accumulation length. Set at initialization.")
parser.add_argument("-g", "--fft_gain", dest="fft_gain", type=int, default=2**15-1,
    help="FFT gain. Set at initialization.")


def main():
    args = parser.parse_args()

    # initialize roach
    roach = cd.initialize_roach(args.ip, boffile=args.boffile, upload=args.upload)

    # useful parameters
    nbrams         = len(args.bramnames) / args.nspecs
    specbrams_list = [args.bramnames[i*nbrams:(i+1)*nbrams] for i in range(args.nspecs)]
    dtype          = '>u' + str(args.dwidth/8)
    nchannels      = 2**args.awidth * nbrams 
    freqs          = np.linspace(0, args.bandwidth, nchannels, endpoint=False)
    dBFS           = 6.02*args.nbits + 1.76 + 10*np.log10(nchannels)

    # create figure
    fig, lines = create_figure(args.nspecs, args.bandwidth, dBFS)
    
    # initial setting of registers
    #print("Setting accumulation register to " + str(args.acclen) + "...")
    #roach.write_int(args.acc_reg, args.acclen)
    #print("done")
    #print("Resseting counter registers...")
    #roach.write_int(args.count_reg, 1)
    #roach.write_int(args.count_reg, 0)
    #print("done")
    #print("writting fft gain")
    #roach.write_int("fft_gain", int(args.fft_gain))

    # animation definition
    def animate(_):
        for line, specbrams in zip(lines, specbrams_list):
            # get spectral data
            specdata = cd.read_interleave_data(roach, specbrams, 
                args.awidth, args.dwidth, dtype)
            specdata = cd.scale_and_dBFS_specdata(specdata, args.acclen, dBFS)
            line.set_data(freqs, specdata)
        return lines

    ani = FuncAnimation(fig, animate, blit=True)
    plt.show()

def create_figure(nspecs, bandwidth, dBFS):
    """
    Create figure with the proper axes settings for plotting spectra.
    """
    axmap = {1 : (1,1), 2 : (1,2), 4 : (2,2), 16 : (4,4)}

    fig, axes = plt.subplots(*axmap[nspecs], squeeze=False)
    fig.set_tight_layout(True)

    lines = []
    for i, ax in enumerate(axes.flatten()):
        ax.set_xlim(0, bandwidth)
        ax.set_ylim(-dBFS-2, 0)
        ax.set_xlabel('Frequency [MHz]')
        ax.set_ylabel('Power [dBFS]')
        ax.set_title('In ' + str(i))
        ax.grid()

        line, = ax.plot([], [], animated=True)
        lines.append(line)

    return fig, lines

if __name__ == '__main__':
    main()

