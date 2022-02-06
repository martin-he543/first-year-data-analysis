import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.constants import pi as π
from scipy.signal import argrelextrema

def fAmplitude(w, N, w0, γ):                                                                                 # Functions found in lab manuals (equation 1.1, 1.10)
    return N/((w**2-w0**2)**2+(γ*w)**2)**0.5
def fPhase(w, w0, γ1,c):
    return np.fmod(np.arctan((-γ1*w)/(w0**2-w**2))+np.pi,np.pi)+c #should be -np.pi

graphDirectory = "Lab/Term 2/2022.02.03 LCR - Computing/"

# Adjust your font settings
titleFont = {'fontname':'Bodoni 72','size':13}
axesFont = {'fontname':'CMU Sans Serif','size':9}
ticksFont = {'fontname':'DM Mono','size':7}
errorStyle = {'mew':1,'ms':3,'capsize':3,'color':'blue','ls':''}
pointStyle = {'mew':1,'ms':3,'color':'blue'}
lineStyle = {'linewidth':0.5}
resistorNames = ['1Ω','2Ω','3Ω']
linspaceRanges = [[62831.85,138230],[62831.85,138230],[62831.85,138230]]
# [102000,50,200]
p0Amplitude = [[102000,50,200],[105000,100000,400000],[102000,50,200]]
# [106000,200,0]
p0Phase = [[100000,200,0],[106000,2000,3.14],[106000,2000,3.14]]
DataPaths = ['1-ohm.csv','2-ohm.csv','3-ohm.csv']

for i in range(3):
    f,φ,φσ,A,Aσ  = np.loadtxt(r"Lab/Term 2/" + DataPaths[i], unpack=True, delimiter = ',')
    ω = 2*π*f*1000          # Note frequency is in kHz
    φ = -φ*π/180             # Convert phase shift into radians
    φσ = φσ*π/180           # Scale standard deviation
    
    X = np.linspace(linspaceRanges[i][0],linspaceRanges[i][1],num=10000)

    #sigma=Aσ, absolute_sigma=False
    curvefitA, cov_curvefitA = curve_fit(fAmplitude, ω, A, p0=p0Amplitude[i])
    plt.xlabel("Angular Frequency, ω / radians.s¯¹", **axesFont)
    plt.ylabel("Amplitude, A / mV", **axesFont)
    plt.xticks(**ticksFont)
    plt.yticks(**ticksFont)
    plt.title("Data for " + resistorNames[i] + " Resistor, Amplitude", **titleFont) 
    plt.errorbar(ω,A,yerr=Aσ,**errorStyle)
    plt.plot(ω,A,'x',**pointStyle)
    plt.plot(X,fAmplitude(X,*curvefitA),'r',**lineStyle)
    #plt.savefig(graphDirectory+"amplitude - "+resistorNames[i]+".png", dpi = 1000)
    plt.show()

    print("Data for " + resistorNames[i] + " Resistor")
    print('N = ',curvefitA[0],'±', np.sqrt(cov_curvefitA[0,0]),'; w0 = ',curvefitA[1],'±',np.sqrt(cov_curvefitA[1,1]),'; γ = ',curvefitA[0],'±',np.sqrt(cov_curvefitA[2,2]))

    # Δω calculation
    Y = fAmplitude(X, *curvefitA)
    rms_max_Y1 = (1/(2**0.5))*np.amax(fAmplitude(X, *curvefitA))
    indices = []
    for j in range(len(Y)):
        if  Y[j]/rms_max_Y1 > 0.999 and Y[j]/rms_max_Y1 < 1.001:
            indices.append(j)
         
    bandwidth = X[indices[-1]] - X[indices[0]]
    print('Bandwidth: ',bandwidth)
    print('Q (experimental) = ', np.abs(curvefitA[1])/bandwidth)

    #print("Resonant Frequency of " + resistorNames[i] + " Resistor:",curvefitA[0]/(2*π))
    
    #sigma=φσ, absolute_sigma=True
    curvefitP, cov_curvefitP = curve_fit(fPhase, ω, φ, sigma = φσ, absolute_sigma = True, p0=p0Phase[i])
    plt.xlabel("Angular Frequency, ω / radians.s¯¹", **axesFont)
    plt.ylabel("Phase Shift, φ / radians", **axesFont)
    plt.xticks(**ticksFont)
    plt.yticks(**ticksFont)
    plt.title("Data for " + resistorNames[i] + " Resistor, Phase Difference", **titleFont) 
    plt.errorbar(ω,φ,yerr=φσ,**errorStyle)
    plt.plot(ω,φ,'x',**pointStyle)
    plt.plot(X,fPhase(X,*curvefitP),'r',**lineStyle)
    #plt.savefig(graphDirectory + "phase - " + resistorNames[i] + ".png", dpi = 1000)
    plt.show()

    print('ω₀ = ',curvefitA[0],'±', np.sqrt(cov_curvefitA[0,0]),'; γ = ',curvefitA[1],'±',np.sqrt(cov_curvefitA[1,1]))


