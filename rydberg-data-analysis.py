import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi as π
from scipy.optimize import curve_fit
import uncertainties as unc
from uncertainties import umath
from uncertainties import ufloat
def functionLinear(try_x,try_m,try_c):              # Curve fit to linear function
    return try_m*try_x + try_c
                                                    ## ADJUST PARAMETERS
d = 1/(78.8*1000)                                   # When using the slit grating of 80 lines per mm
# Adjust your font settings
titleFont = {'fontname':'Bodoni 72','size':13}
axesFont = {'fontname':'CMU Sans Serif','size':9}
ticksFont = {'fontname':'DM Mono','size':7}
errorStyle = {'mew':1,'ms':3,'capsize':3,'color':'blue','ls':''}
pointStyle = {'mew':1,'ms':3,'color':'blue'}
lineStyle = {'linewidth':0.5}
table,errorbarsRed,errorbarsCyan,errorbarsViolet = [],[],[],[]
filePaths = ["rydberg_red_corrected.csv","rydberg_cyan_corrected.csv","rydberg_violet_corrected.csv"]
colourNames,label = ["Red","Cyan","Violet"],["n=3","n=4","n=5"]

# PLOT YOUR GRAPHS [NEW METHOD]:
# Input Rydberg Data in 4 columns of a CSV: (m) - Minima Order; (θ) - sin(Angle) / radians; 
# (θmin/θmax) - absolute differences between sin(min) and sin(max from sin(mean)
for i in range(3):
    errorbars,absoluteError = [],[]
    m,θ,θErrorMin,θErrorMax = np.loadtxt(r"Lab/Term 2/2022.01.20 Rydberg Constant - Computing/" + filePaths[i], unpack=True, delimiter = ',')
    errorbars.append([*θErrorMin])
    errorbars.append([*θErrorMax])
    for j in range(len(θErrorMin)):
        absoluteError.append((θErrorMin[j]+θErrorMax[j])/2)
    curvefit,cov_curvefit = curve_fit(functionLinear,m,θ,sigma=absoluteError,absolute_sigma=True)
    plt.xlabel("Order of maxima, m", **axesFont)
    plt.ylabel("sin(θ)", **axesFont)
    plt.xticks(**ticksFont)
    plt.yticks(**ticksFont)
    plt.title("Data for " + colourNames[i] +" Light, " + label[i], **titleFont) 
    plt.errorbar(m,θ,yerr=errorbars,**errorStyle)
    plt.plot(m,θ,'x',**pointStyle)
    plt.plot(m,functionLinear(m,*curvefit),'r',**lineStyle)
    plt.show()
    
    print(colourNames[i]+" GRAPH")
    print("USING CURVE_FIT METHOD:")
    print("Covariance Matrix: \n",cov_curvefit)
    print(curvefit[0],"; σ=",np.sqrt(cov_curvefit[0,0]))
    table.append([curvefit[0],np.sqrt(cov_curvefit[0,0])])    

## FINAL GRAPHS
## Error Propagation
gradient_red,gradient_cyan,gradient_violet = ufloat(table[0][0],table[0][1]),ufloat(table[1][0],table[1][1]),ufloat(table[2][0],table[2][1])
unc_red,unc_cyan,unc_violet = (d*gradient_red),(d*gradient_cyan),(d*gradient_violet)
sigma_red,sigma_cyan,sigma_violet = 1/(d*gradient_red),1/(d*gradient_cyan),1/(d*gradient_violet)
sigmaError = [sigma_red.s,sigma_cyan.s,sigma_violet.s]

print("\nRed λ:",unc_red,"; Cyan λ:",unc_cyan,"; Violet λ:",unc_violet)
print("Errors (σ) in 1/λ respectively:",sigmaError)

red,cyan,violet = 1/(d*gradient_red._nominal_value),1/(d*gradient_cyan._nominal_value),1/(d*gradient_violet._nominal_value)
x,y = [1/9 - 1/4, 1/16 - 1/4, 1/25 - 1/4],[red,cyan,violet]
s = np.poly1d(x)

print("USING CURVE_FIT METHOD:")
curvefit,cov_curvefit = curve_fit(functionLinear,x,y,sigma=sigmaError,absolute_sigma=True)
plt.xlabel("x, 1/n² - 1/p² / dimensionless", **axesFont)
plt.ylabel("1/λ / m¯¹", **axesFont)
plt.xticks(**ticksFont)
plt.yticks(**ticksFont)
plt.ticklabel_format(style='plain')
plt.title("Rydberg Constant, Determination Graph", **titleFont) 
plt.errorbar(x,y,yerr=sigmaError,**errorStyle)
plt.plot(x,y,'x',**pointStyle)
plt.plot(s,curvefit[0]*s+curvefit[1],'r',**lineStyle)
plt.show()
print("Covariance Matrix: \n",cov_curvefit)
print("Rydberg Constant: ",-curvefit[0],"; σ=",np.sqrt(cov_curvefit[0,0]))
print("End")






