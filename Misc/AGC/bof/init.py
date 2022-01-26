import corr, time
import numpy as np
import calandigital as calan
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



roach_ip = '192.168.0.40'
boffile = 'agc_2.bof.gz'

snapnames = ['snapshot', 'snapshot1', 'reduced', 'gain_out']
snap_dtype = ['>i1', '>i1','>i2', '>u2']
nsamples = 128

#snap_width = [8, 8, 16,  16]
#snap_pt = [7, 7, 8, 8]

snap_width = [8, 8, 16,  16]
snap_pt = [7, 7, 8, 8]

#configure settings 
#ref_pow = fix16_14; error_coef = fix16_8
ref_pow = np.array(0.025)#np.array(0.025)	#this is the reference power ie A**2/2
error_coef = np.array(2)


##init roach
roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)


#create plot
fig, axes = plt.subplots(*(2,2), squeeze=False)
fig.set_tight_layout(True)

lines = []
for snap, ax, width, pt in zip(snapnames, axes.flatten(), snap_width, snap_pt):
    ax.set_xlim(0, nsamples)
    ax.set_ylim((-2,2))#-2.**(width-1))/2**(pt)-2, (2.**(width)-1)/2**(pt)+2)
    ax.set_xlabel("Samples")
    ax.set_ylabel("Amplitud [au]")
    ax.set_title(snap)
    ax.grid()
    line, = ax.plot([],[], animated=True)
    lines.append(line)



roach.write_int('control', 1)   #rst

##write reference power and error coeficient (learning rate)
ref_pow_fix = calan.float2fixed(ref_pow, 16,14)
error_coef_fix = calan.float2fixed(error_coef, 16,8)

roach.write_int('ref_pow', ref_pow_fix)
roach.write_int('error_coef', error_coef_fix)
time.sleep(1)

#enable triggers and agc
roach.write_int('snap_trig', 1)
roach.write_int('control', 0)
roach.write_int('control', 2)   #enable agc


def animate(_):
    #snaplist_b = np.array(calan.read_snapshots(roach, snapnames[0:2], snap_dtype[0]))
    #snaplist_h = np.array(calan.read_snapshots(roach, [snapnames[2]], snap_dtype[2]))
    snaplist_b = np.array(calan.read_snapshots(roach, snapnames[0:3], snap_dtype[0]))
    gain_data = np.array(calan.read_data(roach, snapnames[3], 10 ,snap_width[3], snap_dtype[3]))
    #print(snaplist_b[0].shape)
    #print(snaplist_b[1].shape)
    #print(snaplist_h[0].shape)
    #print(gain_data.shape)
    print(gain_data[0]/2.**snap_pt[3])
    lines[0].set_data(range(nsamples), snaplist_b[0][:nsamples]/2.**snap_pt[0])
    lines[1].set_data(range(nsamples), snaplist_b[1][:nsamples]/2.**snap_pt[1])
    #lines[2].set_data(range(nsamples), snaplist_h[0][:nsamples]/2.**snap_pt[2])
    lines[2].set_data(range(nsamples), snaplist_b[2][:nsamples]/2.**snap_pt[2])
    lines[3].set_data(range(nsamples), gain_data[:nsamples]/2.**snap_pt[3])
    return lines

ani = FuncAnimation(fig, animate, blit=True)
plt.show()





