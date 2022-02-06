import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi as π
from scipy.optimize import curve_fit
import uncertainties as unc
from uncertainties import umath
from uncertainties import ufloat
from uncertainties import unumpy as unp

graphDirectory, g = "Lab/Term 2/Pendulum Graphs/", 9.81
#plotTitle = 'Experiment 1: Angular Amplitude vs. Period, Data Series 1'
plotTitle = 'Experiment 1: Angular Amplitude vs. Period, Data Series 2'
#plotTitle = 'Experiment 2: Density vs. Period¯²'

# Adjust your font settings
titleFont = {'fontname':'Bodoni 72','size':13}
axesFont = {'fontname':'CMU Sans Serif','size':9}
ticksFont = {'fontname':'DM Mono','size':7}
errorStyle = {'mew':1,'ms':3,'capsize':3,'color':'blue','ls':''}
pointStyle = {'mew':1,'ms':3,'color':'blue'}
lineStyle = {'linewidth':0.5,'color':'red'}

# Define necessary functions
def experimentA(θₒ,Tₒ,a,b):
    return Tₒ* (1 + a*θₒ+ b*θₒ**2)                                            
def experimentB(x,m,c):
    return m*x+c

# Import data, and separate into columns
#xData,y1,y2,y3,y1Error,y2Error,y3Error = np.loadtxt(r"Lab/Term 2/pendulum.csv", unpack=True, delimiter = ',',max_rows=6)                # Import for A.1
xData,y1,y2,y3,y1Error,y2Error,y3Error = np.loadtxt(r"Lab/Term 2/pendulum.csv", unpack=True, delimiter = ',',max_rows=5,skiprows=6)    # Import for A.2
#xData,y1,y2,y3,y1Error,y2Error,y3Error = np.loadtxt(r"Lab/Term 2/pendulum.csv", unpack=True, delimiter = ',',max_rows=4,skiprows=11)   # Import for B

# Uncertainty array definitions - N.B. this section is hard-coded since np.array is stupid
#u_yData = np.array([ufloat(0,0),ufloat(0,0),ufloat(0,0),ufloat(0,0),ufloat(0,0),ufloat(0,0)])
u_yData = np.array([ufloat(0,0),ufloat(0,0),ufloat(0,0),ufloat(0,0),ufloat(0,0)])
#u_yData = np.array([ufloat(0,0),ufloat(0,0),ufloat(0,0),ufloat(0,0)])
#u_yData_n = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
u_yData_n = np.array([0.0,0.0,0.0,0.0,0.0])
#u_yData_n = np.array([0.0,0.0,0.0,0.0])
#u_yData_s = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
u_yData_s = np.array([0.0,0.0,0.0,0.0,0.0])
#u_yData_s = np.array([0.0,0.0,0.0,0.0])
#u_xData_n = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
u_xData_n = np.array([0.0,0.0,0.0,0.0,0.0])
#u_xData_n = np.array([0.0,0.0,0.0,0.0])
#u_xData_s = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
u_xData_s = np.array([0.0,0.0,0.0,0.0,0.0])
#u_xData_s = np.array([0.0,0.0,0.0,0.0])

''' # For Experiment 1.1
u_xData = np.array([ufloat(xData[0],2),ufloat(xData[1],2),ufloat(xData[2],2),ufloat(xData[3],2),ufloat(xData[4],2),ufloat(xData[5],2)]) # We defined ± 2° uncertainty
u_y1 = np.array([ufloat(y1[0],y1Error[0]),ufloat(y1[1],y1Error[1]),ufloat(y1[2],y1Error[2]),ufloat(y1[3],y1Error[3]),ufloat(y1[4],y1Error[4]),ufloat(y1[5],y1Error[5])])
u_y2 = np.array([ufloat(y2[0],y2Error[0]),ufloat(y2[1],y2Error[1]),ufloat(y2[2],y2Error[2]),ufloat(y2[3],y2Error[3]),ufloat(y2[4],y2Error[4]),ufloat(y2[5],y2Error[5])])
u_y3 = np.array([ufloat(y3[0],y3Error[0]),ufloat(y3[1],y3Error[1]),ufloat(y3[2],y3Error[2]),ufloat(y3[3],y3Error[3]),ufloat(y3[4],y3Error[4]),ufloat(y3[5],y3Error[5])])
 '''
# For Experiment 1.2
u_xData = np.array([ufloat(xData[0],2),ufloat(xData[1],2),ufloat(xData[2],2),ufloat(xData[3],2),ufloat(xData[4],2)])
u_y1 = np.array([ufloat(y1[0],y1Error[0]),ufloat(y1[1],y1Error[1]),ufloat(y1[2],y1Error[2]),ufloat(y1[3],y1Error[3]),ufloat(y1[4],y1Error[4])])
u_y2 = np.array([ufloat(y2[0],y2Error[0]),ufloat(y2[1],y2Error[1]),ufloat(y2[2],y2Error[2]),ufloat(y2[3],y2Error[3]),ufloat(y2[4],y2Error[4])])
u_y3 = np.array([ufloat(y3[0],y3Error[0]),ufloat(y3[1],y3Error[1]),ufloat(y3[2],y3Error[2]),ufloat(y3[3],y3Error[3]),ufloat(y3[4],y3Error[4])])

 # For Experiment 2
''' u_xData = np.array([ufloat(xData[0],0.2),ufloat(xData[1],0.2),ufloat(xData[2],0.2),ufloat(xData[3],0.2)])
u_y1 = np.array([ufloat(y1[0],y1Error[0]),ufloat(y1[1],y1Error[1]),ufloat(y1[2],y1Error[2]),ufloat(y1[3],y1Error[3])])
u_y2 = np.array([ufloat(y2[0],y2Error[0]),ufloat(y2[1],y2Error[1]),ufloat(y2[2],y2Error[2]),ufloat(y2[3],y2Error[3])])
u_y3 = np.array([ufloat(y3[0],y3Error[0]),ufloat(y3[1],y3Error[1]),ufloat(y3[2],y3Error[2]),ufloat(y3[3],y3Error[3])]) '''


# "Create" uncertainty mean array for Y Data, as well as arrays for just the mean values to plot, and the mean values to 
for i in range(len(u_xData)):
    #print((u_y1[i]+u_y2[i]+u_y3[i])/3)
    averageValue = (u_y1[i] + u_y2[i] + u_y3[i])/3
    # Add to three uncertainty mean array
    u_yData[i] = ufloat(averageValue.nominal_value,averageValue.s)
    u_yData_n[i] = u_yData[i].nominal_value
    u_yData_s[i] = u_yData[i].s
    #print((u_yData[i]).nominal_value)
    #print((u_yData[i]).s)
    u_xData_n[i] = u_xData[i].nominal_value
    u_xData_s[i] = u_xData[i].s

# Graph for Experiment 1.1 and 1.2
curvefitA,cov_curvefitA = curve_fit(experimentA, u_xData_n,u_yData_n,sigma=u_yData_s,absolute_sigma=True)
plt.xlabel("Angular Amplitude, θ initial / °)", **axesFont)
plt.ylabel("Period, T / s", **axesFont)
plt.xticks(**ticksFont)
plt.yticks(**ticksFont)
plt.title(plotTitle, **titleFont) 
plt.errorbar(u_xData_n, u_yData_n, xerr = u_xData_s, yerr = u_yData_s,  **errorStyle)
plt.plot(u_xData_n, u_yData_n,'x',**pointStyle)
plt.plot(u_xData_n, experimentA(u_xData_n, *curvefitA),**lineStyle)
plt.savefig(graphDirectory+plotTitle+".png", dpi = 1000)
plt.show()

# Graph for Experiment 2
''' u_yData_n = u_yData_n**-2
u_yData_s = 2 * u_yData_s
curvefitB, cov_curvefitB = curve_fit(experimentB, u_xData_n,u_yData_n)

plt.xlabel("Density of Pendulum Bob, ρ / g.cm¯³", **axesFont)
plt.ylabel("Period¯², T¯² / s¯²", **axesFont)
plt.xticks(**ticksFont)
plt.yticks(**ticksFont)
plt.title('Experiment B: Density against 1/Period¯²', **titleFont) 
plt.errorbar(u_xData_n, u_yData_n, xerr=u_xData_s, yerr = u_yData_s, **errorStyle)
plt.plot(u_xData_n, u_yData_n,'x',**pointStyle)
plt.plot(u_xData_n, experimentB(u_xData_n, curvefitB[0],curvefitB[1]),**lineStyle)
plt.savefig(graphDirectory+plotTitle+".png", dpi = 1000)
plt.show()

print("Experiment 2:")
print(cov_curvefitB)
print(curvefitB) '''

print("End")
