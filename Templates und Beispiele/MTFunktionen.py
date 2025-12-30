# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 08:36:52 2025

@author: Guehmann, Clemens; TU Berlin, Fachgebiet MDT
Funktionen für die Messtechniksimulation 

    
ADU3Bit(Uin:float) -> int:
    realisiert einen 3-Bit-Analog-Digital-Umsetzer mit differenzieller Nichtlinearität. 
    Der EIngangsspannungsbereich liegt zwischen 0 V und 5 V
    Input: U - Float 
    Output: D - Integer

 
Tiefpassfilter(f0:float, uIn:float, time:float) -> Tuple[np.ndarray, np.ndarray]:   
    realisiert ein Tiefpassfilter zweiter Ordnung mit der Grenzfrequenz f0.
    Input: uIn: Array der Eingansfunktion, time: Array des Zeitvektor, Uin und 
            time müssen die gleiche Dimension besitzen
    Outout: uOut: Array mit den gefilterten Eingangswerten, time Array mit dem
            Zeitvektor, der etwas verändert sein kann

PPT100Viertelbruecke(N:int,Theta:float) -> tuple[np.ndarray, np.ndarray]:
    realisaiert eine Viertelbrücke mit PT100. 
    Input:  Anzahl der Messwerte N und Temperatur Theta
    Output: Array mit Brückenspannung (verrauscht) der Diemansion N 
            Array mit Zeitvektor der Dimension N in der Schrittweite 1e-3 s

Wienbruecke(C2:float, R2:float,R3:float,R4:float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]
    realisiert eine Wien-Messbrücke. Das unbekannte Element ist Z1. Die 
    Speisespannung ist ein Sinus mit 10 V Amplitude und 1000 Hz. Es werden 
    immer 10 ms simuliert. 
    Input: C2,R2,R3,R4 Werte für die trimmbaren Elemente
    Output: Uin: Array der Eingangsspannung, Ub: Array der Brückenspannung, 
            time: Array des Zeitvektors
    
Leistungsmessung(N) -> Tuple[np.ndarray, np.ndarray,np.ndarray, np.ndarray]:
    realisiert die Leistungsmessung an einer ohmsch-induktiven Last. Es werden
    die Effektivwerte von Strom und Spannung gemessen und die Wirkleistung. Alle
    drei Größen sind verrauscht. 
    Input: N: Anzahl der Messwerte
    Output: P: Array der Wirkleistung mit N Messwerten
            Ieff: Array der Stromeffektivwerte mit N Messwerten
            Ueff: Array der Spannungseffektivwerte mit N Messwerten
            time: Array des Zeitvektors mit N Messwerten

"""
# Dieser Pfad muss angepasst werden. Tragen Sie hier den Pfad zu den Datein mit den FMUs ein. 
FMUPath = "C:/Users/Guehmann/Nextcloud/Lehre/01 MT1/Klausuren/HausarbeitPruefung/"

from typing import Tuple
import numpy as np
from fmpy import simulate_fmu


def ADU3Bit(Uin:float) -> int:
    
    # Filename der FMU
    Filename = FMUPath+"ADU3BitDNL1.fmu"
    
    # Obwohl nur ein Wert ausgegeben wird, benötigt die FMU Arrays aus Zeit und Spannungswerten als Eingabe
    time = np.arange(0,10e-6, 1e-6)
    N = time.size
    input_values = np.ones(N)*Uin # Wert ist konstant

    # Name der Eingangsvariablen (aus der FMU-Beschreibung auslesen)
    input_name = "Vin"  # <- Diesen Namen anpassen

    input_data = np.zeros(len(time), dtype=[('time', np.float64), (input_name, np.float64)])
    input_data['time'] = time
    input_data[input_name] = input_values

    # FMU simulieren
    result = simulate_fmu(Filename, start_time=0, stop_time=0.001,input=input_data)
    D = result['D']  # Ausgangsvariable
    return int(D[0]) 



def Tiefpassfilter(f0:float, uIn:float, time:float) -> Tuple[np.ndarray, np.ndarray]:

    # Filename der FMU 
    Filename = FMUPath+"filterButter.fmu"
    
    # Zeitvektor erzeugen
    N = len(time)
    step = time[2]-time[1]
    start_time = 0.0
    stop_time = N*step
    time = np.arange(0,stop_time, step)
    
 
    # Eingangsvariable 
    input_values = uIn

    # Name der Eingangsvariablen (aus der FMU-Beschreibung auslesen)
    input_name = "u1"  # <- Diesen Namen anpassen

    input_data = np.zeros(len(time), dtype=[('time', np.float64), (input_name, np.float64)])
    input_data['time'] = time
    input_data[input_name] = input_values
    
    # FMU simulieren
    result = simulate_fmu(Filename, start_time=start_time, stop_time=stop_time,step_size=step,input=input_data)
    time = result['time']  # Zeitwerte extrahieren
    uOut = result['y1']  # 
    
    # Äquidisdante Schrittweite erzeugen 
    index = (np.diff(time) > step/3).nonzero()
    time = time[index]
    uOut = uOut[index]
    return uOut, time

def PT100Viertelbruecke(N:int,Theta:float) -> Tuple[np.ndarray, np.ndarray]:

    # Filename der  FMU 
    filename = FMUPath+"PT100Bruecke.fmu"
    
    # Zeitvektor erzeugen
    step = 1e-3
    stop_time = N*step
    time = np.arange(0,stop_time, step)
    input_values = np.ones(N)*Theta
 
   
    # Eingangsvariable definieren Temperatur
    input_values = np.ones(len(time))*Theta

    # Name der Eingangsvariablen (aus der FMU-Beschreibung auslesen)
    input_name = "Theta"  # Eingang Temperatur 


    input_data = np.zeros(len(time), dtype=[('time', np.float64), (input_name, np.float64)])
    input_data['time'] = time
    input_data[input_name] = input_values
    
    
    # FMU simulieren
    result = simulate_fmu(filename, start_time=0.0, stop_time=stop_time,step_size=step,input=input_data)
    time = result['time']  # Zeitwerte extrahieren
    ub = result['ub']  # 
    
    # Äquidisdante Schrittweite erzeugen 
    index = (np.diff(time) > step/3).nonzero()
    time = time[index]
    ub = ub[index]
    return ub, time

def Wienbruecke(C2:float, R2:float,R3:float,R4:float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    
    # Filename der FMU 
    filename = FMUPath+"WienBruecke.fmu"
    
    start_values = {
        # Parmeter
        'C2_C':     (C2, 'F'),  # Kapazitaet C2
        'R2_R':     (R2, 'Ohm'),   # Widerstand R2
        'R3_R':     (R3, 'Ohm'),  # Widerstand R3
        'R4_R':     (R4, 'Ohm'),  # Widerstand R4
    }

    output = [
        'Ub',   # Ub
        'Uin',  # Uin
    ]
    
    #Zeitvektor erzeugen
    step = 1e-6
    stop_time =0.02
    time = np.arange(0,stop_time, step)
   
   
    input_data = np.zeros(len(time), dtype=[('time', np.float64)])
    input_data['time'] = time
    
    # FMU simulieren
    result = simulate_fmu(filename, start_time=0.0,start_values=start_values ,stop_time=stop_time,step_size=step,input=input_data)    
    time = result['time']  # Zeitwerte extrahieren
    ub = result['Ub']  # 
    uIn = result['Uin']
    
    return uIn, ub, time



def Leistungsmessung(N) -> Tuple[np.ndarray, np.ndarray,np.ndarray, np.ndarray]:
  
    # Dateiname der FMU
    Filename = FMUPath+"Leistungsmessung.fmu" 
    
    # Eingangsgrößen und Simulationsdauer definieren
    step = 1e-3
    stop_time = N*20e-3+20e-3
    time = np.arange(0,stop_time, step)

 
 
    input_data = np.zeros(len(time), dtype=[('time', np.float64)])
    input_data['time'] = time
 
    # FMU simulieren
    result = simulate_fmu(Filename, step_size=step, start_time=0, stop_time=stop_time,input=input_data)
    time = result['time']  # Zeitwerte extrahieren
    Pw = result['Wirkleistung']  # 
    Ieff = result['Ieff']
    Ueff = result['Ueff']
    
    # Äquidisdante Schrittweite erzeugen 
    index = (np.diff(time) > step/3).nonzero()
    time = time[index]
    Pw = Pw[index]
    Ieff = Ieff[index]
    Ueff = Ueff[index]
    
    # da mit 1E-3 s simuliert wird und alle 20 ms ein Wert ausgegeben werden
    # soll, jeden 20ten Wert herausnehmen
    Pw = Pw[::20];
    time = time[::20]
    Ieff = Ieff[::20]
    Ueff = Ueff[::20]
    return Pw[1:], Ieff[1:],Ueff[1:], time[:-1]

