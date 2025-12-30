# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 17:20:34 2025

@author: Guehmann
"""

import matplotlib.pyplot as plt
import numpy as np
from MTFunktionen import Wienbruecke
plt.close('all')
font = {'family': 'sans-serif',
        'color':  'darkblue',
        'weight': 'normal',
        'size': 20}

#                        C2   R2   R3   R4                        
Uin,Ub,time=Wienbruecke(1e-6,100,1000,1000)
plt.figure(1)
plt.clf()
plt.plot(Ub, Uin, label="Lissayou")
plt.xlabel("Ub [V]",fontdict=font)
plt.ylabel("Uin [V]",fontdict=font)
plt.title("FMU Simulation Result")
plt.legend()
plt.axis( [-12,12,-12,12] ) 
plt.grid()
plt.show()

plt.figure(2)
plt.clf()
plt.plot(time,Ub, label="Ub")
plt.xlabel(" Zeit [s]")
plt.ylabel("Ub [V]")
plt.title("FMU Simulation Result")
plt.legend()
plt.grid()
plt.show()