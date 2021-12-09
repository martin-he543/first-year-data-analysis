# Data extracted using: https://ij.imjoy.io/
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import argrelextrema
from scipy.constants import pi as π
import uncertainties as unc
from uncertainties import ufloat

distanceSS,grayValueSS = np.loadtxt(r"2021.11.18 Diffraction - Computing/single-slit-profile.csv",delimiter=",",skiprows=1,unpack=True,max_rows=1276)
distanceDS,grayValueDS = np.loadtxt(r"2021.11.18 Diffraction - Computing/double-slit-profile-1.csv",delimiter=",",skiprows=1,unpack=True,max_rows=1276)
font = {'fontname':'CMU Serif'}                                                                             # Assign font parameters
fontAxesTicks = {'size':7}

def functionSS(x,I0,a,λ,f):                                                                                 # Functions found in lab manuals (equation 1.1, 1.10)
    return I0*(((np.sin((π*a*x)/(λ*f)))/((π*a*x)/(λ*f)))**2)                                                # SS = Single Slit, DS = Double Slit
def functionDS(x,I0,a,λ,f,d):
    return 4*I0*(((np.sin((π*a*x)/(λ*f)))/((π*a*x)/(λ*f)))**2*((np.cos(π*d*x)/(λ*f))**2))
def functionSSCorrected(x,I0,a,λ,f,φ,k):                                                                    # Perform manual corrections to curve_fit line of best fit for Single Slit and Double Slit
    return k*I0*(((np.sin((π*a*(x-φ))/(λ*f)))/((π*a*(x-φ))/(λ*f)))**2)                                      # "φ" denotes phase shift, "k" denotes vertical scale factor, "ω" denotes horizontal scale factor
def functionDSCorrected(x,I0,a,λ,f,d,φ,k,ω):                                                                # Phase Shift Formula: k(ωx - φ)
    return 4*I0*k*(((np.sin((π*a*(ω*x-φ))/(λ*f)))/((π*a*(ω*x-φ))/(λ*f)))**2*((np.cos(π*d*(ω*x-φ))/(λ*f))**2))
#def slitSeparationSS:
#def slitWidthDS:

    ## SINGLE SLIT EXPERIMENT
distanceSS = 0.0254*distanceSS - (np.mean(0.0254*distanceSS))                                               # Convert to distance from central maxima, (m)
grayValueSS = grayValueSS/np.amax(grayValueSS)
curvefitSS,cov_curvefitSS = curve_fit(functionSS, distanceSS, grayValueSS)                                  # curve_fit finds line of best fit
plt.xlabel("Distance from Central Maximum Peak (x) / m", **font)                                            # Label axes, add titles and error bars
plt.ylabel("Pixel Intensity / Relative", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
plt.title("Single Slit, Profile Plot", **font)
plt.errorbar(distanceSS, grayValueSS, yerr=0.001,xerr=0.0008,ls='',mew=1.5,ms=3,capsize=3)                  # Plots uncertainties in points
plt.plot(distanceSS, functionSSCorrected(distanceSS, *curvefitSS, -0.0025,1.03),'r')                         # (φ,k)
plt.show()                                                                                                  # Show the graphs

pointsY,localminX,increments = [],[],np.linspace(-0.168672,0.168672,num=10000)                              # Numerical method to find minimum of curve_fit
for i in range(len(increments)):                                                                            # Loop for values (accurate to 4.d.p)
    pointsY.append(functionSSCorrected(increments[i],curvefitSS[0],curvefitSS[1],curvefitSS[2],curvefitSS[3],-0.0025,1.03))      # (φ,k)
pointsY = np.array(pointsY)                                                                                 # Convert to a Numpy array
localminY = argrelextrema(pointsY, np.less)                                                                 # Find local minima using argelextrema
for j in range(len(localminY)):                                                                             # Loop around for number of local minima found
    localminX.append(increments[localminY[j]])                                                              # Add the x values of these minima to localminX
localminX = np.reshape(localminX,(4,1))

minimaOrderSS = [-2,-1,1,2]                                                                                 # Order of minima in graph
polyfitSS,cov_polyfitSS = np.polyfit(minimaOrderSS,localminX,1,cov=True)                                    # Polyfit a linear line of best fit
plt.plot(minimaOrderSS, localminX, 'x')                                                                     # Plot the points onto the linear plot
plt.plot(minimaOrderSS, (polyfitSS[0]*minimaOrderSS+polyfitSS[1]))                                          # Plot the line of best fit
plt.xlabel("Order of Minima (n)", **font)                                                                   # Label axes, add titles, errorbars
plt.ylabel("Displacement from Central Maximum Peak (x) / m", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
#plt.errorbar(distanceSS, grayValueSS, yerr=0.001,xerr=0.0008,ls='',mew=1.5,ms=3,capsize=3)                  # Plots uncertainties in linear plot points
plt.title("Single Slit, Minima Plot", **font)
plt.show()                                                                                                  # Show the graphs

    ## DOUBLE-SLIT EXPERIMENT
mean = np.mean(0.0254*distanceDS)
distanceDS = 0.0254*distanceDS - (np.mean(0.0254*distanceDS)) - 0.00254
grayValueDS = 10.49*(grayValueDS/(np.amax(grayValueDS)))
#grayValueDS = grayValueDS/np.amax(grayValueDS)
curvefitDS,cov_curvefitDS = curve_fit(functionDS,distanceDS,grayValueDS,maxfev=1000000)
plt.xlabel("Distance (x) / m", **font)
plt.ylabel("Pixel Intensity / Relative", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks, color='white')
plt.title("Double Slit, Profile Plot", **font)
plt.errorbar(distanceDS, grayValueDS, yerr=0.001,xerr=0.0008,ls='',mew=1.5,ms=3,capsize=3)                  # Plots uncertainties in points
plt.plot(distanceDS, functionDSCorrected(distanceDS, *curvefitDS,-0.004,1.2,1.03),'r',color='red',ms=2,mew=3)
plt.show()

pointsY,localminX,increments = [],[],np.linspace(-0.171212,0.171212,num=10000)
for i in range(len(increments)):                                                                            # Loop for values (accurate to 4.d.p)
    pointsY.append(functionDSCorrected(increments[i],curvefitDS[0],curvefitDS[1],curvefitDS[2],curvefitDS[3],curvefitDS[4],-0.004,1.2,0.97))    # (φ,k,ω)
pointsY = np.array(pointsY)                                                                                 # Convert to a Numpy array
localminY = argrelextrema(pointsY, np.less)                                                                 # Use Dani's method for finding local minima
for j in range(len(localminY)):                                                                             # Loop around for number of local minima found
    localminX.append(increments[localminY[j]])                                                              # Add the x values of these minima to localminX
localminX = np.reshape(localminX,(16,1))

minimaOrderDS = [-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8]                                                   # Order of minima in graph
plt.plot(minimaOrderDS, localminX, 'x')                                                                     # Plot the points onto the linear plot
polyfitDS,cov_polyfitDS = np.polyfit(minimaOrderDS, localminX, 1, cov=True)                                 # Plot the line of best fit
plt.plot(minimaOrderDS, (polyfitDS[0]*minimaOrderDS+polyfitDS[1]))
plt.xlabel("Order of mimima (n)", **font)
plt.ylabel("Displacement from Central Maximum Peak (x) / m", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
#plt.errorbar(distanceDS, grayValueDS, yerr=0.001,xerr=0.0008,ls='',mew=1.5,ms=3,capsize=3)                  # Plots uncertainties in linear plot points
plt.title("Double Slit, Minima Plot", **font)
plt.show()

    ## DATA ANALYSIS: SINGLE SLIT
print('\nSINGLE SLIT DIFFRACTION:')
print('Gradient: %.3e' %(polyfitSS[0]*1.1))                                                                 # Displays the gradient of linear plot, with manual corrections (i.e. k) taken into account
print('The slit seperation (d) / m: %.3e' %(float(670e-9*0.15/(polyfitSS[0]))))                         # Calculates the subsequent slit separation / mm

    ## DATA ANALYSIS: DOUBLE SLIT
print('\nDOUBLE SLIT DIFFRACTION:')
print('Gradient: %.3e' %(polyfitDS[0]*1.2/0.97))                                                            # Displays the gradient of linear plot, with manual corrections (i.e. k,ω) taken into account
print('The slit seperation (d) / m: %.3e' %(float(670e-9*0.15/(polyfitDS[0]))))

    ## UNCERTAINTY PROPAGATION
#σcurvefitSS_I0,σcurvefitSS_a,σcurvefitSS_λ,σcurvefitSS_f = np.sqrt(float(cov_curvefitSS[0][0])),np.sqrt(float(cov_curvefitSS[1][1])),np.sqrt(float(cov_curvefitSS[2][2])),np.sqrt(float(cov_curvefitSS[3][3]))
#σpolyfitSS_X,σpolyfitSS_Y = np.sqrt(float(cov_polyfitSS[0][0])),np.sqrt(float(cov_polyfitSS[1][1]))
#σcurvefitDS_I0,σcurvefitDS_a,σcurvefitDS_λ,σcurvefitDS_f,σcurvefitDS_d = np.sqrt(float(cov_curvefitDS[0][0])),np.sqrt(float(cov_curvefitDS[1][1])),np.sqrt(float(cov_curvefitDS[2][2])),np.sqrt(float(cov_curvefitDS[3][3])),np.sqrt(float(cov_curvefitDS[4][4]))
#σpolyfitDS_X,σpolyfitDS_Y = np.sqrt(float(cov_polyfitDS[0][0])),np.sqrt(float(cov_polyfitDS[1][1]))

uf_λ = ufloat(670e-9,1e-9)                                                                                      # N.B: σ from absolute error (xᵢ-x) of 1e-9 m is also 1e-9 m
uf_f = ufloat(500e-3,0.001)                                                                                            # 670±1nm, f = 500±5 (a unitless ratio)
##  Yaar's value = 0.15
uf_optimal_I0SS = ufloat(curvefitSS[0],np.sqrt(cov_curvefitSS[0,0]))
uf_optimal_aSS = ufloat(curvefitSS[1],np.sqrt(cov_curvefitSS[1,1]))
uf_optimal_λSS = ufloat(curvefitSS[2],np.sqrt(cov_curvefitSS[2,2]))
uf_optimal_fSS = ufloat(curvefitSS[3],np.sqrt(cov_curvefitSS[3,3]))
uf_gradientSS = ufloat(polyfitSS[0],np.sqrt(cov_polyfitSS[0,0]))
uf_yInterceptSS = ufloat(polyfitSS[1],np.sqrt(cov_polyfitSS[1,1]))

uf_optimal_I0DS = ufloat(curvefitDS[0],np.sqrt(cov_curvefitDS[0,0]))
uf_optimal_aDS = ufloat(curvefitDS[1],np.sqrt(cov_curvefitDS[1,1]))
uf_optimal_λDS = ufloat(curvefitDS[2],np.sqrt(cov_curvefitDS[2,2]))
uf_optimal_fDS = ufloat(curvefitDS[3],np.sqrt(cov_curvefitDS[3,3]))
uf_optimal_dDS = ufloat(curvefitDS[4],np.sqrt(cov_curvefitDS[4,4]))
uf_gradientDS = ufloat(polyfitDS[0],np.sqrt(cov_polyfitDS[0,0]))
uf_yInterceptDS = ufloat(polyfitDS[1],np.sqrt(cov_polyfitDS[1,1]))

uf_aSS = (uf_λ*uf_f)/uf_gradientSS
uf_dDS = (uf_λ*uf_f)/uf_gradientDS

print("\n Single Slit Diffraction:")
print("gradient: ",uf_gradientSS)
print("y-intercept: ",uf_yInterceptSS)
print("a = (",uf_aSS,") m")

print("\n Double Slit Diffraction:")
print("gradient: ",uf_gradientDS)
print("y-intercept: ",uf_yInterceptDS)
print("d = (",uf_dDS,") m")

unc_curvefitSS = uf_optimal_I0DS*(((np.sin((π*uf_optimal_aSS)/(uf_optimal_λSS*uf_optimal_fSS)))/((π*uf_optimal_aSS)/(uf_optimal_λSS*uf_optimal_fSS)))**2)
unc_curvefitDS = 4*uf_optimal_I0DS*(((np.sin((π*uf_optimal_aDS)/(uf_optimal_λDS*uf_optimal_fDS)))/((π*uf_optimal_aSS)/(uf_optimal_λDS*uf_optimal_fDS)))**2*((np.cos(π*uf_optimal_dDS)/(uf_optimal_λDS*uf_optimal_fDS))**2))

## COVARIANCE MATRICES
''' print(curvefitSS)
print(polyfitSS)
print(curvefitDS)
print(polyfitDS)
print(cov_curvefitSS)
print(cov_polyfitSS)
print(cov_curvefitDS)
print(cov_polyfitDS) '''