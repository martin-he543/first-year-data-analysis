# Data extracted using: https://ij.imjoy.io/
# Working in metres, NOT millimetres
import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
from scipy.optimize import curve_fit
from scipy.signal import argrelextrema
from scipy.constants import pi as π
import uncertainties as unc
from uncertainties import umath
from uncertainties import ufloat

distanceSS,grayValueSS = np.loadtxt(r"2021.11.18 Diffraction - Computing/single-slit-profile.csv",delimiter=",",skiprows=1,unpack=True,max_rows=1276)
distanceDS,grayValueDS = np.loadtxt(r"2021.11.18 Diffraction - Computing/double-slit-profile-1.csv",delimiter=",",skiprows=1,unpack=True,max_rows=1276)
SSCorrections,DSCorrections = [-0.0025,1.03],[-0.004,1.2,1.03,0.00254]                                      # Corrections to curve_fit
font,fontAxesTicks,fontAxesTitles,fontTitles = {'fontname':'CMU Serif'},{'size':10,'rotation':0},{'size':11},{'size':12}      # Assign font parameters
f,λ = 500e-3,670e-9
diffConst = π/(f*λ)
CMOS_PixelSize=5.2e-6
CMOS_ScalingFactor = 1
#CMOS_ScalingFactor=2.643749843e-4/CMOS_PixelSize
SSRange,DSRange = [-0.168672*CMOS_ScalingFactor,0.168672*CMOS_ScalingFactor],[-0.13*CMOS_ScalingFactor,0.165*CMOS_ScalingFactor]    # Search ranges for minima
#distanceSS,distanceDS = distanceSS*CMOS_ScalingFactor,distanceDS*CMOS_ScalingFactor

def functionSS(x,I0,a):                                                                                     # Functions found in lab manuals (equation 1.1, 1.10)
    return I0*(((np.sin((diffConst*a*x)))/(diffConst*a*x))**2)                                              # SS = Single Slit, DS = Double Slit
def functionDS(x,I0,a,d):
    return 4*I0*(((np.sin((diffConst*a*x)))/(diffConst*a*x))**2)*((np.cos(diffConst*d*x)**2))
def functionSSCorrected(x,I0,a,φ,k):                                                                        # Perform manual corrections to curve_fit line of best fit for Single Slit and Double Slit
    return k*I0*(((np.sin((diffConst*a*(x-φ))))/(diffConst*a*(x-φ)))**2)                                    # "φ" denotes phase shift, "k" denotes vertical scale factor, "ω" denotes horizontal scale factor
def functionDSCorrected(x,I0,a,d,φ,k,ω):                                                                    # Phase Shift Formula: k(ωx - φ)
    return 4*k*I0*(((np.sin((diffConst*a*(ω*x-φ))))/(diffConst*a*(ω*x-φ)))**2)*((np.cos(diffConst*d*(ω*x-φ))**2))

    ## SINGLE SLIT EXPERIMENT
distanceSS = 0.0254*distanceSS - (np.mean(0.0254*distanceSS))                                               # Convert to distance from central maxima, (m)
grayValueSS = grayValueSS/np.amax(grayValueSS)
curvefitSS,cov_curvefitSS = curve_fit(functionSS, distanceSS, grayValueSS,p0=[1,1e-6*CMOS_ScalingFactor])                      # curve_fit finds line of best fit
plt.xlabel("Displacement from Central Maximum Peak (x) / mm", **font,**fontAxesTitles)                                            # Label axes, add titles and error bars
plt.ylabel("Pixel Intensity / Relative", **font,**fontAxesTitles)
plt.xticks([-0.15,-0.10,-0.05,0,0.05,0.10,0.15],[-4.36,-2.91,-1.45,0,1.45,2.91,4.36],**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
plt.title("Single Slit, Profile Plot", **font, **fontTitles)
plt.errorbar(distanceSS, grayValueSS, yerr=0.001,xerr=0.0008,ls='',mew=1.5,ms=3,capsize=3)                  # Plots uncertainties in points
plt.plot(distanceSS, functionSSCorrected(distanceSS, *curvefitSS, SSCorrections[0],SSCorrections[1]),'r')   # (φ,k)
plt.show()                                                                                                  # Show the graphs

pointsY,localminX,increments = [],[],np.linspace(SSRange[0],SSRange[1],num=10000)                           # Numerical method to find minimum of curve_fit
for i in range(len(increments)):                                                                            # Loop for values (accurate to 4.d.p)
    pointsY.append(functionSSCorrected(increments[i],curvefitSS[0],curvefitSS[1],SSCorrections[0],SSCorrections[1]))
pointsY = np.array(pointsY)                                                                                 # Convert to a Numpy array
localminY = argrelextrema(pointsY, np.less)                                                                 # Find local minima using argelextrema
for j in range(len(localminY)):                                                                             # Loop around for number of local minima found
    localminX.append(increments[localminY[j]])                                                              # Add the x values of these minima to localminX
localminX = np.reshape(localminX,(4,1))

minimaOrderSS = [-2,-1,1,2]                                                                                 # Order of minima in graph
polyfitSS,cov_polyfitSS = np.polyfit(minimaOrderSS,localminX,1,cov=True)                                    # Polyfit a linear line of best fit
plt.plot(minimaOrderSS, localminX, 'x')                                                                     # Plot the points onto the linear plot
plt.plot(minimaOrderSS, (polyfitSS[0]*minimaOrderSS+polyfitSS[1]))                                          # Plot the line of best fit
plt.xlabel("Order of Minima (n)", **font,**fontAxesTitles)                                                                   # Label axes, add titles, errorbars
plt.ylabel("Displacement from Central Maximum Peak (x) / mm", **font,**fontAxesTitles)
plt.xticks(**font, **fontAxesTicks)
plt.yticks([-0.15,-0.10,-0.05,0,0.05,0.10,0.15],[-4.36,-2.91,-1.45,0,1.45,2.91,4.36],**font, **fontAxesTicks)
plt.title("Single Slit, Minima Plot", **font, **fontTitles)
plt.show()                                                                                                  # Show the graphs

    ## DOUBLE-SLIT EXPERIMENT
mean=np.mean(0.0254*distanceDS)
distanceDS = 0.0254*distanceDS - (np.mean(0.0254*distanceDS)) - DSCorrections[3]
#grayValueDS = 10.49*(grayValueDS/(np.amax(grayValueDS)))
grayValueDS = grayValueDS/np.amax(grayValueDS)
curvefitDS,cov_curvefitDS = curve_fit(functionDS,distanceDS,grayValueDS,p0=[1,1e-6*CMOS_ScalingFactor,1e-5*CMOS_ScalingFactor])
plt.xlabel("Displacement from Central Maximum Peak (x) / mm", **font,**fontAxesTitles)
plt.ylabel("Pixel Intensity / Relative", **font,**fontAxesTitles)
plt.xticks([-0.15,-0.10,-0.05,0,0.05,0.10,0.15],[-4.36,-2.91,-1.45,0,1.45,2.91,4.36],**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
plt.title("Double Slit, Profile Plot", **font, **fontTitles)
plt.errorbar(distanceDS, grayValueDS, yerr=0.001,xerr=0.0008,ls='',mew=1.5,ms=3,capsize=3)                  # Plots uncertainties in points
plt.plot(distanceDS, functionDSCorrected(distanceDS, *curvefitDS,DSCorrections[0],DSCorrections[1],DSCorrections[2]),'r',color='red',ms=2,mew=3)
plt.show()

pointsY,localminX,increments = [],[],np.linspace(DSRange[0],DSRange[1],num=10000)
for i in range(len(increments)):                                                                            # Loop for values (accurate to 4.d.p)
    pointsY.append(functionDSCorrected(increments[i],curvefitDS[0],curvefitDS[1],curvefitDS[2],DSCorrections[0],DSCorrections[1],DSCorrections[2]))
pointsY = np.array(pointsY)                                                                                 # Convert to a Numpy array
localminY = argrelextrema(pointsY, np.less)                                                                 # Use Dani's method for finding local minima
for j in range(len(localminY)):                                                                             # Loop around for number of local minima found
    localminX.append(increments[localminY[j]])                                                              # Add the x values of these minima to localminX
localminX = np.reshape(localminX,(len(localminX[0]),1))

minimaOrderDS = [-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8]                                                   # Order of minima in graph
plt.plot(minimaOrderDS, localminX, 'x')                                                                     # Plot the points onto the linear plot
polyfitDS,cov_polyfitDS = np.polyfit(minimaOrderDS, localminX, 1, cov=True)                                 # Plot the line of best fit
plt.plot(minimaOrderDS, (polyfitDS[0]*minimaOrderDS+polyfitDS[1]))
plt.xlabel("Order of mimima (n)", **font,**fontAxesTitles)
plt.ylabel("Displacement from Central Maximum Peak (x) / mm", **font,**fontAxesTitles)
plt.xticks(**font, **fontAxesTicks)
plt.yticks([-0.15,-0.10,-0.05,0,0.05,0.10,0.15],[-4.36,-2.91,-1.45,0,1.45,2.91,4.36],**font, **fontAxesTicks)
plt.title("Double Slit, Minima Plot", **font, **fontTitles)
plt.show()

    ## ERROR PROPAGATION
uf_λ = ufloat(670e-9,1e-9)                                                                                  # N.B: σ from absolute error (xᵢ-x) of 1e-9 m is also 1e-9 m
uf_f = ufloat(500e-3,10e-3)                                                                                 # 670±1nm, f = 500±5 (a unitless ratio)
##  Yaar's value = 0.15
uf_optimal_I0SS = ufloat(curvefitSS[0],np.sqrt(cov_curvefitSS[0,0]))
uf_optimal_aSS = ufloat(curvefitSS[1],np.sqrt(cov_curvefitSS[1,1]))
uf_optimal_λSS = ufloat(670e-9,1e-9)
uf_optimal_fSS = ufloat(500e-3,0.001)
uf_gradientSS = ufloat(polyfitSS[0],np.sqrt(cov_polyfitSS[0,0]))
uf_yInterceptSS = ufloat(polyfitSS[1],np.sqrt(cov_polyfitSS[1,1]))

uf_optimal_I0DS = ufloat(curvefitDS[0],np.sqrt(cov_curvefitDS[0,0]))
uf_optimal_aDS = ufloat(curvefitDS[1],np.sqrt(cov_curvefitDS[1,1]))
uf_optimal_λDS = ufloat(670e-9,1e-9)
uf_optimal_fDS = ufloat(500e-3,0.001)
uf_optimal_dDS = ufloat(curvefitDS[2],np.sqrt(cov_curvefitDS[2,2]))
uf_gradientDS = ufloat(polyfitDS[0],np.sqrt(cov_polyfitDS[0,0]))
uf_yInterceptDS = ufloat(polyfitDS[1],np.sqrt(cov_polyfitDS[1,1]))

uf_aSS = (uf_λ*uf_f)/(uf_gradientSS)
uf_dDS = (uf_λ*uf_f)/(uf_gradientDS)

print("\n Single Slit Diffraction:")
print("gradient: ",uf_gradientSS)
print("y-intercept: ",uf_yInterceptSS)
print("a = (",uf_aSS*34.4,") m")

print("\n Double Slit Diffraction:")
print("gradient: ",uf_gradientDS)
print("y-intercept: ",uf_yInterceptDS)
print("d = (",uf_dDS*47.5,") m")

unc_curvefitSS = uf_optimal_I0DS*(((umath.sin((π*uf_optimal_aSS)/(uf_optimal_λSS*uf_optimal_fSS)))/((π*uf_optimal_aSS)/(uf_optimal_λSS*uf_optimal_fSS)))**2)
unc_curvefitDS = 4*uf_optimal_I0DS*(((umath.sin((π*uf_optimal_aDS)/(uf_optimal_λDS*uf_optimal_fDS)))/((π*uf_optimal_aSS)/(uf_optimal_λDS*uf_optimal_fDS)))**2*((umath.cos(π*uf_optimal_dDS)/(uf_optimal_λDS*uf_optimal_fDS))**2))

print(unc_curvefitSS)
print(unc_curvefitDS)

