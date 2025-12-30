# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 08:51:47 2025

@author: Guehmann
"""

from MTFunktionen import PT100Viertelbruecke
import matplotlib.pyplot as plt
import numpy as np

plt.close('all')

# Vorgabe der Temeperatur

Theta = 100
ub,time = PT100Viertelbruecke(100,Theta)

plt.figure()
plt.step(time, ub)
plt.ylabel("uB (V)")
plt.xlabel("Zeit (s)")
plt.title("FMU Simulation Result")
plt.grid()
plt.show()
