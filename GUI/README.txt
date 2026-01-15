"""
Um fmpy.simulate_fmu bei mir auf Windows zu nutzen, musste ein Windows-Subsystem für Linux(wsl) installieren.

So habe ich es gemacht:
"""


wsl.exe --install

wsl.exe --list --online

-> Ubuntu (oder andere dist aussuchen)

wsl.exe --install Ubuntu-24.04



--------------------------------------------------------------------------------

main_gui.py ist der entrypoint. 
Also:

1. venv mit python 3.11.4 erstellen(oder global installieren)

2. benötigte libraries installieren (pip install ...): 

pillow
customtkinter
matplotlib
fmpy

3. main_gui.py ausführen
