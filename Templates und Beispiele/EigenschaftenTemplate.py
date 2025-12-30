# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 11:37:38 2025

@author: Guehmann
"""

import matplotlib.pyplot as plt
import numpy as np
from MTFunktionen import Tiefpassfilter
plt.close('all')


# Eingangsgrößen und Simulationsdauer definieren
stop_time = 0.002 # Länge der Simulation
step = 1e-6 # Schrittweite der Simulation. Nicht verändern!
time = np.arange(0,stop_time, step) # Zeitvektor für die Simulation

# Eingangsvariable definieren (z.B. Sinus)
uIn = np.sin(time*6.28*1000)
f0 = 1000 # 3dB-Grenzfrequenz
uOut,time= Tiefpassfilter(f0,uIn,time) # Filter wird simuliert


# Plot erzeugen
plt.figure(1)
plt.plot(time, uOut)
plt.xlabel("Time (s)")
plt.ylabel("Value")
plt.title("FMU Simulation Result")
plt.grid()
plt.show()
