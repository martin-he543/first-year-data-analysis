import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy.constants import pi as π
from scipy import optimize


# Adjust your font settings
titleFont = {'fontname':'Bodoni 72','size':13}
axesFont = {'fontname':'CMU Sans Serif','size':9}
ticksFont = {'fontname':'DM Mono','size':7}
errorStyle = {'mew':1,'ms':3,'capsize':3,'color':'blue','ls':''}
pointStyleOne = {'mew':1,'ms':1,'color':'blue'}
pointStyleTwo = {'mew':1,'ms':1,'color':'red'}
lineStyle = {'linewidth':1}
figureFont = font_manager.FontProperties(family="DM Mono", size=7)
dataPath = ['sine','sine-aluminium','sine-copper','sine-ferrous','sine-steel','rectangular','triangular','exponential','ramp']
titles = ['Sine Wave','Sine Wave (with Aluminium Core)','Sine Wave (with Copper Core)','Sine Wave (with Iron Core)','Sine Wave (with Mild Steel Core)','Rectangular Wave','Triangular Wave','Exponential Wave','Ramp Wave']
graphDirectory = 'Term 2/2022.02.10 Faraday - Computing/'

def sineCurve(t, A, w, p, c):  
    return A * np.sin(w*t + p) + c
def fastFourier(tt, yy):
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])

    popt, pcov = optimize.curve_fit(sineCurve, tt, yy, p0=guess)
    print(popt)
    print(pcov)
    print('A=',popt[0],'±',np.sqrt(pcov[0,0]))
    print('w=',popt[1],'±',np.sqrt(pcov[1,1]))
    print('p=',popt[2],'±',np.sqrt(pcov[2,2]))
    print('c=',popt[3],'±',np.sqrt(pcov[3,3]))
    A, w, p, c = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}

for i in range(len(dataPath)):
    t,channelOne,channelTwo = np.loadtxt(r"Lab/" + graphDirectory + dataPath[i] + ".CSV",unpack=True,delimiter=',',skiprows=1)
    #channelTwo = channelTwo*100
    title = "Oscilloscope Trace for " + titles[i]
    print(title)
    plt.xlabel("Time (s)", **axesFont)
    plt.ylabel("Voltage / V", **axesFont)
    plt.xticks(**ticksFont)
    plt.yticks(**ticksFont)
    plt.title(title, **titleFont) 
    #plt.errorbar(m,θ,yerr=errorbars,**errorStyle)
    #plt.plot(t,channelOne,'x',**pointStyleOne)
    #plt.plot(t,channelTwo,'x',**pointStyleTwo)
    
    res = fastFourier(t, channelTwo)
    #print("Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res)
    #plt.plot(t, channelTwo, "-k", label="y", linewidth=2)
    plt.plot(t, channelTwo, "x", label="Channel 1, Voltage Output", **pointStyleOne)
    plt.plot(t, res["fitfunc"](t), "r-", label="Channel 1, Curve Fit", **lineStyle)
    plt.legend(loc="lower right",prop=figureFont)
    #plt.savefig(r"Lab/" + graphDirectory + "channel-1 - " + title + ".png",dpi=500)
    plt.show()

    #params,params_cov = optimize.curve_fit(sinusodial, t, channelOne)
    #plt.plot(t, sinusodial(t,*params),'r', **lineStyle)
    #print(params)
    #print(params_cov)
    #plt.show()
    #plt.figure().clear()
    #plt.close()
    #plt.cla()
    #plt.clf()



