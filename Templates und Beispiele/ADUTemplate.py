# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 08:51:47 2025

@author: Guehmann
"""

from MTFunktionen import ADU3Bit
import matplotlib.pyplot as plt
import numpy as np

plt.close('all')

# Erstes Besipiel der Anwendungsbeispiel
D = ADU3Bit(-0.1)
test_values = [ 0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
print([ADU3Bit(v) for v in test_values])


# Jetzt in einer Schleife etwas mehr Werte erzeugen
# Anzahl der Punkte
N = 50
# Eingangswerte erzeugen
Uin = 2.51*np.sin(np.arange(0,N)/N*20e-3*6.28*50)+2.5 # sinus ist willkürlich gewählt
D = np.zeros(N)

for k in range(0, N):
    D[k]=ADU3Bit(Uin[k]) 
    
# Plot erzeugen
plt.figure(1)
plt.plot(Uin, D)
plt.xlabel("U (V)")
plt.ylabel("D")
plt.title("FMU Simulation Result")
plt.grid()
plt.show()
