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
    angle_1 = peak_power(rp)
    t1 = 0
    t2 = 0
    found2 = False
    found3 = False
    
    while (angle_plus(angle_1, t1*10)//10 < 36 and not(found2)):
        found2 = rp[angle_plus(angle_1, t1*10)//10] <= 0.5
        #print ("rp1 = %d" % rp[angle_plus(angle_1, t1)//10])
        if(not(found2)):
            t1 += 1
    
    while (angle_min(angle_1, t2*10)//10 < 36 and not(found3)):
        found3 = rp[angle_min(angle_1, t2*10)//10] <= 0.5
        #print("rp2 = %d" % rp[angle_min(angle_1, t2)//10])
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

    power_azimuth = df['azimuth']
    # power_azimuth = [10**(x/10) for x in df['azimuth']]
    norm_power_azimuth = [x/max(power_azimuth) for x in power_azimuth]

    power_elev = df['elevation']
    # power_elev = [10**(x/10) for x in df['elevation']]
    norm_power_elev= [x/max(power_elev) for x in power_elev]

    solid_angle = np.radians(hpbw(norm_power_azimuth) + hpbw(norm_power_elev))
    peak_directivity = 4*np.pi/solid_angle
    gain = 8
    efficiency = 10**(gain - 10*np.log10(peak_directivity))
    print(gain, 10*np.log10(peak_directivity), efficiency)

    # textbox
    param_azimuth = "Peak power angle = %d \nHPBW = %d" % (peak_power(norm_power_azimuth), hpbw(norm_power_azimuth))
    param_elev = "Peak power angle = %d \nHPBW = %d" % (peak_power(norm_power_elev), hpbw(norm_power_elev))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    # plot setup
    # azimuth
    ax_azimuth = plt.subplot(121, projection='polar')
    ax_azimuth.plot(phi, norm_power_azimuth)
    ax_azimuth.set_theta_zero_location('N')
    ax_azimuth.set_rmax(1)
    ax_azimuth.set_rticks([0.25, 0.5, 0.75, 1])  # less radial ticks
    ax_azimuth.set_rlabel_position(111.5)  # get radial labels away from plotted line
    ax_azimuth.grid(True)
    ax_azimuth.text(-0.25, 0, param_azimuth, transform=ax_azimuth.transAxes, fontsize=12, verticalalignment='top', bbox=props)
    ax_azimuth.set_title("Normalized Radiation Pattern (Azimuth)")

    # elevation
    ax_elev = plt.subplot(122, projection='polar')
    ax_elev.plot(phi, norm_power_elev)
    ax_elev.set_theta_zero_location('N')
    ax_elev.set_rmax(1)
    ax_elev.set_rticks([0.25, 0.5, 0.75, 1])  # less radial ticks
    ax_elev.set_rlabel_position(111.5)  # get radial labels away from plotted line
    ax_elev.grid(True)
    ax_elev.text(-0.25, 0, param_elev, transform=ax_elev.transAxes, fontsize=12, verticalalignment='top', bbox=props)
    ax_elev.set_title("Normalized Radiation Pattern (Elevation)")

    # show plot
    plt.show()