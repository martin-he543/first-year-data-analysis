import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi as π
from scipy.optimize import curve_fit
import uncertainties as unc
from uncertainties import umath
from uncertainties import ufloat
g = 9.81

θ,t,tUncertainty = np.loadtxt(r"Lab/Term 2/2022.01.27 Not So Simple Pendulum - Computing/nss-real-experiment-a.csv", unpack=True, delimiter = ',')

# Adjust your font settings
titleFont = {'fontname':'Bodoni 72','size':13}
axesFont = {'fontname':'CMU Sans Serif','size':9}
ticksFont = {'fontname':'DM Mono','size':7}
errorStyle = {'mew':1,'ms':3,'capsize':3,'color':'blue','ls':''}
pointStyle = {'mew':1,'ms':3,'color':'blue'}
lineStyle = {'linewidth':0.5,'color':'red'}

def experimentA(θₒ,Tₒ,a,b):
    return Tₒ* (1 + a*θₒ+ b*θₒ**2)                                            
def experimentB(x,m,c):
    return m*x+c

curvefitA,cov_curvefitA = curve_fit(experimentA, θ,t)
plt.xlabel("Angular Amplitude, θ initial / °)", **axesFont)
plt.ylabel("Period, T / s", **axesFont)
plt.xticks(**ticksFont)
plt.yticks(**ticksFont)
plt.title('Experiment A: Angular Amplitude vs. Period', **titleFont) 
plt.errorbar(θ, t, yerr = tUncertainty,  **errorStyle)
plt.plot(θ,t,'x',**pointStyle)
plt.plot(θ, experimentA(θ, *curvefitA),**lineStyle)
plt.savefig('Experiment A', dpi = 1000)
plt.show()

print("Experiment A:")
print(cov_curvefitA)
print('a = ', curvefitA[1], 'b = ', curvefitA[2], 'Tₒ = ', curvefitA[0])

# Experiment B
ρ,T,TUncertainty = np.loadtxt(r"Lab/Term 2/2022.01.27 Not So Simple Pendulum - Computing/nss-real-experiment-b.csv", unpack=True, delimiter = ',')   #import values of density and period.
curvefitB, cov_curvefitB = curve_fit(experimentB, ρ, T)
TSquared = 1/T**2

plt.xlabel("Density of Pendulum Bob, ρ / g.cm¯³", **axesFont)
plt.ylabel("Period¯², T¯² / s¯²", **axesFont)
plt.xticks(**ticksFont)
plt.yticks(**ticksFont)
plt.title('Experiment B: Density against 1/Period¯²', **titleFont) 
plt.errorbar(ρ, TSquared, yerr = TUncertainty, **errorStyle)
plt.plot(ρ, TSquared,'x',**pointStyle)
plt.plot(ρ, experimentB(ρ, curvefitB[0],curvefitB[1]-0.28),**lineStyle)

plt.savefig('Experiment B', dpi = 1000)
plt.show()

print("Experiment B:")
print(cov_curvefitB)
#print('k = ', curvefitB[0])
