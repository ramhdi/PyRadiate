# PyRadiate
# Antenna radiation plotter
# ramhdi, 09/12/2018

# import libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

# angle operation
def angle_plus(a, b):
    r = a+b
    if (r >= 360):
        r -= 360
    return r

def angle_min(a,b):
    r = a-b
    if (r <= 0):
        r += 360
    return r

# function for finding peak power angle
def peak_power(rp):
    t = 0
    found1 = False
    
    while (t < 36 and not(found1)):
        found1 = rp[t] == 1
        
        if(not(found1)):
            t += 1

    return(t*10)

# function for half power beamwidth
def hpbw(rp):
    angle_1 = peak_power(rp)/10
    t1 = 0
    t2 = 0
    found2 = False
    found3 = False
    
    while (int(angle_plus(angle_1, t1)/10) < 36 and not(found2)):
        found2 = rp[int(angle_plus(angle_1, t1)/10)] <= 0.5

        if(not(found2)):
            t1 += 1
    
    while ((angle_min(angle_1, t2)/10) < 36 and not(found3)):
        found3 = rp[int(angle_min(angle_1, t2)/10)] <= 0.5

        if(not(found3)):
            t2 += 1

    t1 -= 1
    t2 -= 1
    return(10*(t1+t2))

# main program
if __name__ == '__main__':
    # open .csv data
    df = pd.read_csv(sys.argv[1])

    # data variables
    phi = np.radians(df['sudut'])
    power = [10**(x/10) for x in df['azimuth']]
    norm_power = [x/max(power) for x in power]

    print("Peak power angle = %f" % (peak_power(norm_power)))
    print("HPBW = %f" % (hpbw(norm_power)))

    # textbox
    param = "Peak power angle = %d \nHPBW = %d" % (peak_power(norm_power), hpbw(norm_power))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    # plot setup
    ax = plt.subplot(111, projection='polar')
    ax.plot(phi, norm_power)
    ax.set_theta_zero_location('N')
    ax.set_rmax(1)
    ax.set_rticks([0.25, 0.5, 0.75, 1])  # less radial ticks
    ax.set_rlabel_position(111.5)  # get radial labels away from plotted line
    ax.grid(True)
    ax.text(-0.25, 0, param, transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props)
    ax.set_title("Normalized Radiation Pattern")

    # show plot
    plt.show()