import numpy as np
import uncertainties as unc
from uncertainties import umath
from uncertainties import ufloat as uf
from uncertainties import unumpy as unp
from scipy.constants import pi as π

Bandwidth = [7065.513206320626,8008.084338433837,9041.14229922992]
R = uf(1,0.01)
#R = uf(2,0.02)
R = uf(3,0.03)

L = uf(0.001,0.0001)
C = uf(100e-9,20e-9)

V0 = ((L*C)**(-0.5))/(2*π)
ω0 = 2*π*V0

QualityFactor = ω0 * L / R
#print(QualityFactor)

Q1 = ω0/Bandwidth[0]
Q2 = ω0/Bandwidth[1]
Q3 = ω0/Bandwidth[2]

print(QualityFactor)
# 100.0+/-11.224972160321824
# 50.0+/-5.612486080160912
# 33.333333333333336+/-3.741657386773941

# 14.153253568409239+/-1.5823818540877266
# 12.487380973257492+/-1.396131635857062
# 11.060549285737657+/-1.2366070035698071
