import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy.constants import pi as π
from scipy.misc import derivative
from scipy import optimize
from scipy import signal

# Adjust your font settings
titleFont = {'fontname': 'Bodoni 72', 'size': 13}
subtitleFont = {'fontname': 'Inter', 'size': 6}
axesFont = {'fontname': 'CMU Sans Serif', 'size': 9}
ticksFont = {'fontname': 'DM Mono', 'size': 7}
errorStyle = {'mew': 1, 'ms': 3, 'capsize': 3, 'color': 'blue', 'ls': ''}
pointStyle = {'mew': 1, 'ms': 3, 'color': 'blue'}
lineStyle = {'linewidth': 0.5}
figureFont = font_manager.FontProperties(family="DM Mono", size=7)
graphDirectory = "Lab/Term 2/"

# Parameters (from left to right):
# nₚ - number of primary coils
# n₅ - number of secondary coils
# f - frequency of signal generator
# vₚ - amplified signal, reaching primary coil
# ε - efficiency
parameters = [100, 50, 500, 2,0.0001]
# start value, stop value, number of intervals (the higher the better)
timeScale = [0, 0.01,100000]
resistors = [18,27]
n_p, n_s, f, v_p, ε = parameters[0], parameters[1], parameters[2], parameters[3], parameters[4]
plotTitles = ["Transformer Trace, Sinusodial Waveform","Transformer Trace, Triangular Waveform"]

def sinusodial(t):
    return v_p*np.sin(2*π*f*t)/resistors[0]
def dSinusodial(t):
    return (ε*v_p*n_s/n_p)*derivative(sinusodial, t, dx=1e-9, n=1)/resistors[1]
def triangular(t):
    return v_p*signal.sawtooth(2*π*f*t, 0.5)/resistors[0]
def dTriangular(t):
    return (ε*v_p*n_s/n_p)*derivative(triangular, t, dx=1e-9, n=1)/resistors[1]
def square(t):
    return v_p*signal.square(2*π*f*t)
def dSquare(t):
    return (ε*v_p*n_s/n_p)*derivative(square, t, dx=1e-9, n=1)/(2*π*f)

time = np.linspace(*timeScale)
title = "nₚ: "+str(n_p)+"; n₅: "+str(n_s)+"; f: "+str(f)+"; vₚ: "+str(v_p)+"; ε: "+str(ε)


'''
A_p = v_p*sinusodial(time)
A_s = ε*v_p*n_s*dSinusodial(time-π/2)/n_p
amp1 = v_p*np.sin(2*np.pi*f*time)/resistors[0]
amp2 = v_s*np.sin(2*np.pi*(f*time)-(π/2))/resistors[1]
plt.plot(time, A_p, 'r', label='Current in Primary Coil', color='blue')
plt.plot(time, A_s, 'r', label='Current Secondary Coil', color='red')
'''

plt.plot(time, sinusodial(time), 'r', label='Current in Primary Coil, I_p', color='blue')
plt.plot(time, dSinusodial(time), 'r', label='Current in Secondary Coil, I_s', color='red')
plt.suptitle(plotTitles[0], **titleFont)
plt.title(title, **subtitleFont)
plt.xlabel("Time, t / s", **axesFont)
plt.ylabel("Current, I /A", **axesFont)
plt.xticks(**ticksFont)
plt.yticks(**ticksFont)
plt.legend(loc="upper right", prop=figureFont)
plt.savefig(graphDirectory + plotTitles[0] + ' - ' + title +'.png', dpi=500)
plt.show()

plt.plot(time,triangular(time),label='Current in Primary Coil, I_p')
plt.plot(time,dTriangular(time),label='Current in Secondary Coil, I_s')
plt.suptitle(plotTitles[1], **titleFont)
plt.title(title, **subtitleFont)
plt.xlabel("Time, t / s", **axesFont)
plt.ylabel("Current, I /A",**axesFont)
plt.xticks(**ticksFont)
plt.yticks(**ticksFont)
plt.legend(loc="upper right", prop=figureFont)
plt.savefig(graphDirectory + plotTitles[1] +' - '+ title +'.png', dpi=500)
plt.show()

''' plt.plot(time,square(time))
plt.plot(time,dSquare(time))
plt.suptitle("Transformer Trace, Rectangular Waveform", **titleFont)
plt.title(title, **subtitleFont)
plt.xlabel("Time, t / s", **axesFont)
plt.ylabel("Current, I /A", **axesFont)
plt.xticks(**ticksFont)
plt.yticks(**ticksFont)
plt.legend(loc="upper right", prop=figureFont)
plt.show() '''