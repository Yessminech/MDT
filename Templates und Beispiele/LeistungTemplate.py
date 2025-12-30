# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 19:06:28 2025

@author: Guehmann
"""

import matplotlib.pyplot as plt
import numpy as np
from MTFunktionen import Leistungsmessung
plt.close('all')
font = {'family': 'sans-serif',
        'color':  'darkblue',
        'weight': 'normal',
        'size': 20}


Pw, Ieff,Ueff, time = Leistungsmessung(100)
# Plot erzeugen
plt.figure()
plt.step(time, Pw, label="Pw")
plt.xlabel("Time (s)")
plt.ylabel("P")
plt.title("FMU Simulation Result")
plt.legend()
plt.grid()

plt.figure()
plt.step(time, Ieff, label="Ieff")
plt.xlabel("Time (s)")
plt.ylabel("Ieff")
plt.title("FMU Simulation Result")
plt.legend()

plt.figure()
plt.step(time, Ueff, label="Ueff")
plt.xlabel("Time (s)")
plt.ylabel("Ueff")
plt.title("FMU Simulation Result")
plt.legend()

plt.show()