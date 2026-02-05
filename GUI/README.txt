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

""""
Ubuntu 22.04.5 LTS (before installing libraries)
""""
Python 3.9.6 was built without Tk support.
sudo apt update
sudo apt install -y tk-dev
sudo apt install -y libsqlite3-dev
pyenv uninstall -f 3.9.6
pyenv install 3.9.6
pyenv rehash

""""
GUI Usage
""""
1. Select FMU (öffnen button)
