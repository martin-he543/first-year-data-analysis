import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import uncertainties as unc
from uncertainties import ufloat

nSS,startPosSS,endPosSS,medPosSS,nSS,xSS,low_xSS,high_xSS = np.loadtxt(r"2021.11.18 Diffraction - Computing/a-single-slit.csv",delimiter=",",skiprows=1,unpack=True)
nDS,startPoDSS,endPoDSS,medPoDSS,nDS,xDS,low_xDS,high_xDS = np.loadtxt(r"2021.11.18 Diffraction - Computing/a-double-slit-2.csv",delimiter=",",skiprows=1,unpack=True)
font = {'fontname':'CMU Serif'}                                                                                 # Assign font parameters
fontAxesTicks = {'size':7}

polyfitSS,cov_polyfitSS = np.polyfit(nSS,xSS,1,cov=True)
plt.plot(nSS, xSS, 'x')
plt.plot(nSS, (polyfitSS[0]*nSS+polyfitSS[1]))
plt.xlabel("Order of Minima (n)", **font)                                                                       # Label axes, add titles, errorbars
plt.ylabel("Displacement from Central Maximum Peak (x) / mm", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
plt.errorbar(nSS,xSS,yerr=low_xSS,xerr=0,ls='',mew=1.5,ms=3,capsize=3)                                          # Plots uncertainties in linear plot points
plt.title("Single Slit, Minima Plot", **font)
plt.show()

polyfitDS,cov_polyfitDS = np.polyfit(nDS,xDS,1,cov=True)                                                        # Polyfit a linear line of best fit
plt.plot(nDS, xDS, 'x')                                                                                         # Plot the points onto the linear plot
plt.plot(nDS, (polyfitDS[0]*nDS+polyfitDS[1]))                                                                  # Plot the line of best fit
plt.xlabel("Order of Minima (n)", **font)                                                                       # Label axes, add titles, errorbars
plt.ylabel("Displacement from Central Maximum Peak (x) / mm", **font)
plt.xticks(**font, **fontAxesTicks)
plt.yticks(**font, **fontAxesTicks)
plt.errorbar(nDS,xDS,yerr=low_xDS,xerr=0,ls='',mew=1.5,ms=3,capsize=3)                                          # Plots uncertainties in linear plot points
plt.title("Double Slit, Minima Plot", **font)
plt.show()

uf_λ = ufloat(670e-6,1e-6)                                                                                      # N.B: σ from absolute error (xᵢ-x) of 1e-9 m is also 1e-9 m
uf_f = ufloat(500,5)                                                                                            # 670±1nm, f = 500±5 (a unitless ratio)
uf_gradientSS = ufloat(polyfitSS[0],np.sqrt(cov_polyfitSS[0,0]))
uf_gradientDS = ufloat(polyfitDS[0],np.sqrt(cov_polyfitDS[0,0]))
uf_yInterceptSS = ufloat(polyfitSS[1],np.sqrt(cov_polyfitSS[1,1]))
uf_yInterceptDS = ufloat(polyfitDS[1],np.sqrt(cov_polyfitDS[1,1]))
uf_aSS = (uf_λ*uf_f)/uf_gradientSS
uf_dDS = (uf_λ*uf_f)/uf_gradientDS

print("\n Single Slit Diffraction:")
print("gradient: ",uf_gradientSS)
print("y-intercept: ",uf_yInterceptSS)
print("a = (",uf_aSS,") mm")

print("\n Double Slit Diffraction:")
print("gradient: ",uf_gradientDS)
print("y-intercept: ",uf_yInterceptDS)
print("d = (",uf_dDS,") mm")