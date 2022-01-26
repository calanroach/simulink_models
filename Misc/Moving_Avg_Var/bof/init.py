import numpy as np
import corr, time, struct
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import calandigital as calan


roach_ip = '192.168.0.40'
boffile = 'avg_pow_spect.bof.gz'
acc_len = 4096#1024
dBFS = 6.02*8 + 10*np.log10(2**11)

#model parameters
y_lim = (260,320)
bram_addr_width = 10
bram_sw_pow = 'spect_pow'
sw_pow_size = 64
sw_pow_point =35
bram_avg = 'mov_avg'
avg_size = 32 # actually is 25
avg_point = 12
bram_var = 'mov_var'
var_size = 64 #actually is 50
var_point = 24

def main():
    roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)
    time.sleep(1)
    fig, lines = create_fig()

    ##set registers
    roach.write_int('cnt_rst',1)
    roach.write_int('acc_len',acc_len)
    roach.write_int('cnt_rst',0)

    ##animation
    def animate(_):
        sw_pow = calan.read_data(roach, bram_sw_pow, bram_addr_width,
                sw_pow_size, '>u8')
        sw_pow = sw_pow/(2.**sw_pow_point)
        hw_avg = calan.read_data(roach, bram_avg, bram_addr_width,
                avg_size, '>u4')
        hw_avg = hw_avg/(2.**avg_point)
        hw_var = calan.read_data(roach, bram_var, bram_addr_width,
                var_size, '>u8')
        hw_var = hw_var/(2.**var_point)
        #pow_db = calan.scale_and_dBFS_specdata(sw_pow, acc_len, dBFS)
        #avg_db = calan.scale_and_dBFS_specdata(hw_avg, acc_len, dBFS)
        #var_db = calan.scale_and_dBFS_specdata(hw_var, acc_len, dBFS)
        #var_db = 10*np.log10(hw_var+1)
        #sw_var = np.var(pow_db)
        #sw_avg = np.mean(pow_db)
        sw_var = np.var(sw_pow)
        sw_avg = np.mean(sw_pow)
        lines[0].set_data(range(len(sw_pow)),sw_pow)        
        lines[1].set_data(range(len(hw_avg)),hw_avg)        
        lines[2].set_data(range(len(hw_var)),hw_var)
        print("sw avg: %.4f \t sw var: %.4f" %(sw_avg, sw_var))
        print("hw avg: %.4f \t hw var: %.4f" %(hw_avg[0], hw_var[0]))
        print("\n")
        return lines

    ani = animation.FuncAnimation(fig, animate, blit=True)
    plt.show()



def create_fig():
    fig = plt.figure()
    axes = []
    lines = []
    ax0 = fig.add_subplot(121)
    ax1 = fig.add_subplot(222)
    ax2 = fig.add_subplot(224)
    ax0.set_xlim(0,2**bram_addr_width)
    ax0.set_ylim(y_lim)
    ax0.grid()
    ax0.set_title('Integ power')

    ax1.set_xlim(0,2**bram_addr_width)
    ax1.grid()
    ax1.set_ylim(y_lim)
    ax1.set_title('Avg')

    ax2.set_xlim(0,2**bram_addr_width)
    ax2.grid()
    ax2.set_ylim(-1,15)
    ax2.set_title('Var')

    line0, = ax0.plot([],[], animated=True)
    line1, = ax1.plot([],[], animated=True)
    line2, = ax2.plot([],[], animated=True)

    lines.append(line0)
    lines.append(line1)
    lines.append(line2)
    return [fig, lines]


if __name__ == '__main__':
    main()

