import numpy as np
from numpy import exp
from numpy import polyfit
from numpy import log
import matplotlib.pyplot as plt

RImageDistance,RObjectDistance,Magnification,ObjectDistance = np.loadtxt(r"2021.11.25 Lenses - Computing/lenses-experiment-a.csv",delimiter=",",skiprows=1,unpack=True) 
font = {'fontname':'CMU Serif'}                                                                             # Assign font parameters
fontAxesTicks = {'size':7}


    ## 1/s against 1/s'
polyfitA,cov_polyfitA = np.polyfit(RObjectDistance,RImageDistance,1,cov=True)
plt.xlabel("Object Distance¯¹ / m¯¹", **font)                                                                        # Label axes, add titles and error bars
plt.ylabel("Image Distance¯¹ / m¯¹", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
plt.title("Experiment A: 1/s against 1/s'", **font)
plt.plot(RObjectDistance,RImageDistance,'x')
plt.plot(RObjectDistance, (polyfitA[0]*RObjectDistance+polyfitA[1]))
plt.show()
print(polyfitA)

polyfitB,cov_polyfitB = np.polyfit(RImageDistance,RObjectDistance,1,cov=True)
plt.xlabel("Image Distance¯¹ / m¯¹", **font)                                                                        # Label axes, add titles and error bars
plt.ylabel("Object Distance¯¹ / m¯¹", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
plt.title("Experiment A: 1/s against 1/s'", **font)
plt.plot(RImageDistance,RObjectDistance,'x')
plt.plot(RImageDistance, (polyfitB[0]*RImageDistance+polyfitB[1]))
plt.show()
print(polyfitB)

    ## M against s
#polyfitB,cov_polyfitB = np.polyfit(b,h,1,cov=True)
plt.xlabel("Object Distance / m", **font)                                                                        # Label axes, add titles and error bars
plt.ylabel("Magnification / no units", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
plt.title("Experiment A: M against s'", **font)
#plt.errorbar(f,e, yerr=((1/(f+0.1))-(1/(f-0.1))),xerr=(1/(e+0.1)-1/(e-0.1)),ls='',mew=1.5,ms=3,capsize=3)                         # Plots uncertainties in points
plt.plot(ObjectDistance,Magnification,'x')
#plt.plot(f, (polyfitA[0]*f+polyfitA[1]))
plt.show()

''' plt.plot(1/objectDistance, 1/imageDistance,'x')
polyfitA,cov_polyfitA = np.polyfit(1/objectDistance,1/imageDistance,2,cov=True)    
#plt.plot(1/objectDistance, (polyfitA[0]*(1/objectDistance)**2+polyfitA[1]*(1/objectDistance)+polyfitA))
plt.xlabel("Time (t) / s", **font)                                                                          # Label axes, add titles and error bars
plt.ylabel("Natural Log of Voltage (ln V) / V", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
#plt.errorbar(distanceDS, grayValueDS,yerr=0,xerr=0,ls='',mew=1.5,ms=3,capsize=3)
plt.title("Small Capacitor, Discharging (Linear)", **font)
plt.show() '''