import numpy as np
from numpy import exp
from numpy import polyfit
from numpy import log
from scipy.constants import pi as π
import matplotlib.pyplot as plt
import uncertainties as unc
from uncertainties import umath
from uncertainties import ufloat

timeLCD,voltageLCD = np.loadtxt(r"2021.11.11 Capacitance - Computing/E3T1C01.csv",delimiter=",",skiprows=42477,unpack=True)     # LCD - Large Capacitor, using Discharge
timeSCD,voltageSCD = np.loadtxt(r"2021.11.11 Capacitance - Computing/Capacitance2.csv",delimiter=",",skiprows=2894,unpack=True) # SCD - Small Capacitor, using Discharge
timeSCP,voltageSCP = np.loadtxt(r"2021.11.11 Capacitance - Computing/E3T1C03.csv",delimiter=",",skiprows=1,unpack=True)         # SCP - Small Capacitor, using Phase Shift
font = {'fontname':'CMU Serif'}                                                                             # Assign font parameters
fontAxesTicks = {'size':7}
def discharge(t,V0,R,C):
    return V0*exp(-t/(R*C))
def dischargeLinear(t,V0,R,C):
    return log(V0)-t/(R*C)
def capacitance(R,gradient):
    return -1/(R*gradient)

    ## EXPERIMENT 1: Large Capacitor Discharging
plt.xlabel("Time (t) / s", **font)                                                                          # Label axes, add titles and error bars
plt.ylabel("Voltage (V) / V", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
plt.title("Large Capacitor, Discharging (Profile)", **font)
plt.plot(timeLCD, voltageLCD,'r')
plt.show()

plt.plot(timeLCD, log(voltageLCD), 'x')                                                                     # Plot the points onto the linear plot
polyfitLCD,cov_polyfitLCD = np.polyfit(timeLCD, log(voltageLCD), 1, cov=True)   
plt.plot(timeLCD, (polyfitLCD[0]*timeLCD+polyfitLCD[1]))
plt.xlabel("Time (t) / s", **font)                                                                          # Label axes, add titles and error bars
plt.ylabel("Natural Log of Voltage (ln V) / V", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
plt.title("Large Capacitor, Discharging (Linear)", **font)
plt.show()


    ## EXPERIMENT 2: Small Capacitor Discharging
plt.xlabel("Time (t) / s", **font)                                                                          # Label axes, add titles and error bars
plt.ylabel("Voltage (V) / V", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
plt.title("Small Capacitor, Discharging (Profile)", **font)
plt.plot(timeSCD, voltageSCD,'r')
plt.show()

plt.plot(timeSCD, log(voltageSCD), 'x')                                                                     # Plot the points onto the linear plot
polyfitSCD,cov_polyfitSCD = np.polyfit(timeSCD, log(voltageSCD), 1, cov=True)   
plt.plot(timeSCD, (polyfitSCD[0]*timeSCD+polyfitSCD[1]))
plt.xlabel("Time (t) / s", **font)                                                                          # Label axes, add titles and error bars
plt.ylabel("Natural Log of Voltage (ln V) / V", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
plt.title("Small Capacitor, Discharging (Linear)", **font)
plt.show()

# DATA ANALYSIS FOR EXPERIMENTS 1 and 2
gradientSCD = ufloat(polyfitSCD[0],np.sqrt(cov_polyfitSCD[0,0]))
gradientLCD = ufloat(polyfitLCD[0],np.sqrt(cov_polyfitLCD[0,0]))
R_LCD = ufloat(10E3,0)          # σ in resistance of resistor used (LCD experiment) unknown
R_SCD = ufloat(100E3,0)         # σ in resistance of resistor used (SCD experiment) unknown

# Gradient represents -1/RC, therefore rearrange for C, C = -1/(R*gradient) 


capacitanceSCD = capacitance(R_SCD,gradientSCD)
capacitanceLCD = capacitance(R_LCD,gradientLCD)
print("Large Capacitor Capacitance: ",capacitanceLCD,"F")
print("Small Capacitor Capacitance: ",capacitanceSCD,"F")

    ## EXPERIMENT 3: Small Capacitor Phase Shift
def totalCapacitance(v,Xc):
    return 1/(2*π*v*Xc)
def totalReactance(Vx,Ig,φ):
    return Vx/(Ig*umath.cos(φ))
def lossAngle(Vg,α,VR1):
    return umath.acos((Vg*umath.sin(α))/VR1)
def currentSuppliedSignalGenerator(VR1,R1):
    return VR1/R1
def resistanceR1(Vg,α,Vx):
    return umath.sqrt((Vg*umath.cos(α)-Vx)**2+(Vg*umath.sin(α))**2)

Vgpeak = ufloat(2.0035,1.1018E-3)
Vxpeak = ufloat(1.5126,4.2401E-3)
Vg,Vx = Vgpeak/2,Vxpeak/2
α = ufloat((360-343.64)*π/180,13.02*π/180)
R1 = ufloat(6.8E3,0)                # σ of resistance R1 unknown, so omitted from calculations
v = ufloat(50E3,0)                  # σ in driving frequency on oscilloscope unknown
C2 = ufloat(20E-12,0)               # Uncertainty in model for capacitance of oscilloscope unknown
R2 = ufloat(1E6,0)

VR1 = resistanceR1(Vg,α,Vx)
Ig = currentSuppliedSignalGenerator(VR1,R1)
φ = lossAngle(Vg,α,VR1)
Xc = totalReactance(Vx,Ig,φ)
C_total = totalCapacitance(v,Xc)

C1 = C_total - C2
print("Small Capacitor Capacitance (using Phase Shift): ",C1,"F")
print("---------------End of Program---------------------")




"""
# EXPERIMENT 3: Small Capacitor Phase Shift
#voltageSCP = voltageSCP + (np.mean(voltageSCP))
voltageSCP = voltageSCP + 0.25
plt.xlabel("Time (t) / s", **font)                                                                           # Label axes, add titles and error bars
plt.ylabel("Voltage (V) / V", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
plt.title("Small Capacitor, Phase Shift", **font)
#plt.errorbar(distanceSS, grayValueSS, yerr=0.001,xerr=0.0008,ls='',mew=1.5,ms=3,capsize=3)                  # Plots uncertainties in points
plt.plot(timeSCP, voltageSCP,'r')
plt.show()
"""

## UNCERTAINTY CALCULATIONS
print(polyfitLCD)
print(cov_polyfitLCD)

print(polyfitSCD)
print(cov_polyfitSCD)