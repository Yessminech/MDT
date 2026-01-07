
"""
@author: David

TODO (David): 
-File-Dialog öffnen und FMU laden
-Buttons im linken Panel einfügen und Funktionen dessen definieren
-Parameter dynamisch laden und veränderbar machen
-start_sim Funktion definieren
"""

import customtkinter as ctk
from tkinter import filedialog
from fmpy import read_model_description, extract, simulate_fmu

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


ctk.set_appearance_mode("dark")   # optionen: light, system, dark
ctk.set_default_color_theme("green")  # optionen: dark-blue, green, etc.


class BaseGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Fenster config 
        self.title("GEM Simulationen")
        self.geometry("1000x600") # m.m.n gute größe, gerne feedback
        self.minsize(900, 500)

        # Main layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # GUI Komponenten erstellen
        self.create_topbar()
        self.create_left_panel()
        self.create_main_view()
        self.create_statusbar()

    
    # topbar aka Menüleiste

    def create_topbar(self):
        self.topbar = ctk.CTkFrame(self, height=50)
        self.topbar.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.topbar.grid_columnconfigure(0, weight=1)

        # Buttons
        btn_open = ctk.CTkButton(self.topbar, text="Öffnen...", width=120, command=self.on_open)
        btn_open.grid(row=0, column=1, padx=10, pady=10)

        btn_help = ctk.CTkButton(self.topbar, text="Info", width=70, command=self.on_info)
        btn_help.grid(row=0, column=2, padx=10, pady=10)

    
    # LINKES PANEL (Parameter)
    
    def create_left_panel(self):
        self.left_panel = ctk.CTkFrame(self, width=250, corner_radius=10)
        self.left_panel.grid(row=1, column=0, sticky="nsw", padx=10, pady=10)

        title = ctk.CTkLabel(self.left_panel, text="Parameter", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        # dynamische Felder für Parameter.
        #Scrollbar? ja? nein? -> gerne feedback
        self.parameter_scroll = ctk.CTkScrollableFrame(self.left_panel, width=230, height=400)
        self.parameter_scroll.pack(pady=5, padx=5, fill="both", expand=True)

        #buttons WORK IN PROGRESS#####################################################
        """
        self.btn_sim = ctk.CTkButton(self.left_panel, text="Sim starten", command=self.run_sim) #start_sim muss definiert werden
        self.btn_sim.pack(pady=10)

        self.parameter_entries = {}

        """



        # placeholder unkommentieren wenn leer
        #placeholder = ctk.CTkLabel(self.left_panel, text="(Parameter hier rein)")
        #placeholder.pack(pady=10)

    
    # HAUPTANSICHT (Plot/Simulation)
    
    def create_main_view(self):
        self.view_frame = ctk.CTkFrame(self, corner_radius=10)
        self.view_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.view_frame.grid_rowconfigure(0, weight=1)
        self.view_frame.grid_columnconfigure(0, weight=1)

        #canvas für den Plot erstellen
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Simulation")
        self.ax.set_xlabel("Zeit")
        self.ax.set_ylabel("Wert")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.view_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # placeholder unkommentieren wenn leer
        #placeholder = ctk.CTkLabel(self.view_frame, text="(Platz für Plot und andere Inhalte)", font=("Arial", 16))
        #placeholder.place(relx=0.5, rely=0.5, anchor="center")

    
    # STATUSBAR
    
    def create_statusbar(self):
        self.status = ctk.StringVar(value="Bereit.")

        status_frame = ctk.CTkFrame(self, height=30, fg_color="gray15")
        status_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        label = ctk.CTkLabel(status_frame, textvariable=self.status)
        label.pack(anchor="w", padx=10)

    
    # Callbacks (platzhalte - nichts implementiert)
   
    def on_open(self):
        self.status.set("Dateien öffnen... (noch nicht implementiert)")

    def on_info(self):
        self.status.set("Info: GUI rennt ganz schnelle.")



