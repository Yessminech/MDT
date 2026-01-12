
"""
@author: David

TODO (David): 
-File-Dialog öffnen und FMU laden [done]
-Buttons im linken Panel einfügen und Funktionen dessen definieren [done]
-Parameter dynamisch laden und veränderbar machen [done]
-start_sim Funktion definieren [done]
-import und simulation von .fmu - Dateien mit fmpy [done]

-Felder für Parameter schöner machen
-mehrere canvas für mehrere Plots gleichzeitig erstellen
-handling für FMUs mit Linux binaries ausdenken
-ausgewaehlte FMUs bereits vorher im Programm integrieren -> Schnellauswahl
-user entschiedet welche Variablen geplottet werden?
-user entschiedet auf welcher achse welcher wert geplottet wird? (outputs, dropdown)

"""

import customtkinter as ctk
from tkinter import filedialog
from fmpy import read_model_description, simulate_fmu

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

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # GUI Komponenten erstellen
        self.create_topbar()
        self.create_left_panel()
        self.create_main_view()
        self.create_statusbar()

        self.fmu_path = None  #Pfad zur geladenen FMU
        self.last_result = None  #Simulationsergebnisse
        #self.model_description = None

    
    # topbar aka Menüleiste

    def create_topbar(self):
        self.topbar = ctk.CTkFrame(self, height=50)
        self.topbar.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Buttons
        btn_open = ctk.CTkButton(self.topbar, text="Öffnen...", width=120, command=self.on_open)
        btn_open.grid(row=0, column=1, padx=10, pady=10)

        btn_help = ctk.CTkButton(self.topbar, text="Info", width=70, command=self.on_info)
        btn_help.grid(row=0, column=2, padx=10, pady=10)

        #notiz: column 0 noch frei

    
    # LINKES PANEL (Parameter)
    
    def create_left_panel(self):
        self.left_panel = ctk.CTkFrame(self, width=250, corner_radius=10)
        self.left_panel.grid(row=1, column=0, sticky="nsw", padx=10, pady=10)

        title = ctk.CTkLabel(self.left_panel, text="Parameter", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        # stop time voreinstellung
        stop_frame = ctk.CTkFrame(self.left_panel)
        stop_frame.pack(fill="x", pady=(0, 8), padx=5)
        stop_label = ctk.CTkLabel(stop_frame, text="Stop time (s):")
        stop_label.pack(side="left", padx=5)
        self.stop_time_entry = ctk.CTkEntry(stop_frame, width=80)
        self.stop_time_entry.pack(side="right", padx=5)
        self.stop_time_entry.insert(0, "1.0")

        # dynamische Felder für Parameter.

        self.parameter_scroll = ctk.CTkScrollableFrame(self.left_panel, width=230, height=350)
        self.parameter_scroll.pack(pady=5, padx=5, fill="both", expand=True)

        #"simulation dtarten"-button
        
        self.btn_sim = ctk.CTkButton(self.left_panel, text="Sim starten", command=self.run_sim)
        self.btn_sim.pack(pady=10)

        self.parameter_entries = {}
    
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

    
    # STATUSBAR
    
    def create_statusbar(self):
        self.status = ctk.StringVar(value="Bereit.")

        status_frame = ctk.CTkFrame(self, height=30, fg_color="gray15")
        status_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        label = ctk.CTkLabel(status_frame, textvariable=self.status)
        label.pack(anchor="w", padx=10)

    
    def create_parameter_fields(self):

        #verherige widgets löschen
        for widget in self.parameter_scroll.winfo_children():
            widget.destroy()
        self.parameter_entries.clear()

        #neue parameter laden
        for var in read_model_description(self.fmu_path).modelVariables:
            if var.causality == "parameter":
                frame = ctk.CTkFrame(self.parameter_scroll)
                frame.pack(fill="x", pady=5, padx=5)

                label = ctk.CTkLabel(frame, text=f"{var.name} ({var.type})")
                label.pack(side="left", padx=5)

                entry = ctk.CTkEntry(frame)
                entry.pack(side="right", padx=5)
                entry.insert(0, str(var.start) if var.start is not None else "0")

                self.parameter_entries[var.name] = entry



    # FMU LADEN UND PARAMETER FELDER ERSTELLEN
   
    def on_open(self):
        path = filedialog.askopenfilename(title="FMU Datei laden", filetypes=[("FMU Dateien", "*.fmu")])
        
        if not path:
            return 0

        self.fmu_path = path

        self.status.set(f"Geladene FMU: {self.fmu_path}")
        self.create_parameter_fields()
       

    #info button
    def on_info(self):
        self.status.set("Info: GUI rennt ganz schnelle.")

    #simulation starten nach knopfdruck
    def run_sim(self):
        if not self.fmu_path:
            self.status.set("Keine FMU geladen.")
            return 0

        self.status.set("Simulation laeuft...")

        #parameter lesen
        start_values = {}
        for name, entry in self.parameter_entries.items():
            try:
                val = float(entry.get())
                start_values[name] = val
            except ValueError:
                self.status.set(f"Ungueltiger Wert für Parameter {name}.")
                return 0

        #stop time checekn
        try:
            stop_time = float(self.stop_time_entry.get())
        except Exception:
            self.status.set("Ungueltiger Wert für stop time.")
            return 0

        #simulieren
        result = simulate_fmu(self.fmu_path, start_values=start_values, stop_time=stop_time)

        self.last_result = result

        #Plot aktualisieren
        self.ax.clear()
        self.ax.plot(result['time'], result[list(result.dtype.names)[1]]) #temporär zum testen, ersten output plotten
        self.ax.set_title("Simulationsergebnisse")
        self.ax.set_xlabel("Zeit")
        self.ax.set_ylabel("Wert")
        self.ax.grid(True)
        self.canvas.draw()

        self.status.set("Simulation abgeschlossen.")
