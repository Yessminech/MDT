
"""
@author: David

TODO (David): 
-File-Dialog öffnen und FMU laden [done] by david
-Buttons im linken Panel einfügen und Funktionen dessen definieren [done] by david
-Parameter dynamisch laden und veränderbar machen [done] by david
-start_sim Funktion definieren [done] by david
-import und simulation von .fmu - Dateien mit fmpy [done] by david

-Felder für Parameter schöner machen [done] by david
-mehrere canvas für mehrere Plots gleichzeitig erstellen [vorerst nicht mehr relevant]
-handling für FMUs mit Linux binaries ausdenken
-ausgewaehlte FMUs bereits vorher im Programm integrieren -> Schnellauswahl [done] by david
-user entscheidet welche Variablen geplottet werden? [done] by david
-user entscheidet auf welcher achse welcher wert geplottet wird? (outputs, dropdown) [done] by david
-zweite y-achse? [done] by david
-mehrere outputs auf einer y-achse [done] by david
-zweite y-achse sperren wenn y1 nicht benutzt [done] by david
-tabs?
"""

import customtkinter as ctk
from tkinter import filedialog
from fmpy import read_model_description, simulate_fmu
import os

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
        self.geometry("1000x700")
        self.minsize(900, 500)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        #schnellauswahl für vorausgewählte FMUs
        self.quick_fmus = {
            "WienBruecke": os.path.join("FMUs", "WienBruecke.fmu"),
            "Leistungsmessung": os.path.join("FMUs", "Leistungsmessung.fmu")
        }

        # GUI Komponenten erstellen
        self.create_topbar()
        self.create_left_panel()
        self.create_main_view()
        self.create_statusbar()

        self.fmu_path = None  #Pfad zur geladenen FMU
        self.last_result = None  #Simulationsergebnisse
        self.model_description = None

        self.ax2 = None #zweite y-Achse




    
    # topbar aka Menüleiste

    def create_topbar(self):
        self.topbar = ctk.CTkFrame(self, height=50)
        self.topbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.topbar.pack_propagate(False)



        # Buttons
        btn_open = ctk.CTkButton(self.topbar, text="Öffnen...", width=120, command=self.on_open)
        btn_open.pack(side="right", padx=5, pady=2)

        btn_help = ctk.CTkButton(self.topbar, text="Info", width=70, command=self.on_info)
        btn_help.pack(side="right", padx=5, pady=2)

        # schnellauswahl button
        self.quick_menu = ctk.CTkOptionMenu(self.topbar, values=["Beispiele"] + list(self.quick_fmus.keys()), command=self.on_quick_select)
        self.quick_menu.pack(side="left", padx=5, pady=2)

    
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

        self.parameter_scroll = ctk.CTkScrollableFrame(self.left_panel, width=230, height=210)
        self.parameter_scroll.pack(pady=5, padx=5, fill="both", expand=True)

        #"simulation dtarten"-button
        
        self.btn_sim = ctk.CTkButton(self.left_panel, text="Sim starten", command=self.run_sim)
        self.btn_sim.pack(pady=10)

        self.parameter_entries = {}

        # dropdown für achsen
        plot_frame = ctk.CTkFrame(self.left_panel, height=250)
        plot_frame.pack(fill="x", pady=(0, 8), padx=5)
        plot_frame.pack_propagate(False)

        ctk.CTkLabel(plot_frame, text="Plot Einstellungen").pack(pady=(5,2), anchor = "w", padx=5)

        #x-Achse dropdown
        x_axis = ctk.CTkFrame(plot_frame)
        x_axis.pack(fill="x", pady=(2,2), padx=5)
        ctk.CTkLabel(x_axis, text="X-Achse:").pack(side="left", padx=5)

        self.x_var = ctk.StringVar(value="time")
        self.x_dropdown = ctk.CTkOptionMenu(x_axis, variable=self.x_var, values=["time"])
        self.x_dropdown.pack(side="right", fill="x")


        #y-Achse dropdown
        y_axis = ctk.CTkFrame(plot_frame)
        y_axis.pack(fill="x", pady=(2,2), padx=5)
        ctk.CTkLabel(y_axis, text="Y-Achse:").pack(side="left", padx=5)

        self.y_var = ctk.StringVar(value="none")
        self.y_dropdown = ctk.CTkOptionMenu(y_axis, variable=self.y_var, values=["none"])
        self.y_dropdown.pack(side="right", fill="x")


        #y-Achse 2 dropdown
        y2_axis = ctk.CTkFrame(plot_frame)
        y2_axis.pack(fill="x", pady=(2,2), padx=5)
        ctk.CTkLabel(y2_axis, text="Y-Achse 2:").pack(side="left", padx=5)

        self.y2_var = ctk.StringVar(value="none")
        self.y2_dropdown = ctk.CTkOptionMenu(y2_axis, variable=self.y2_var, values=["none"])
        self.y2_dropdown.pack(side="right", fill="x")

        #änderung y-achse checken
        self.y_var.trace_add("write", self.y_change)

        #boxen für weitere outputs
        ctk.CTkLabel(plot_frame, text="weitere Outputs plotten").pack(anchor = "w", padx=5, pady=(5,2))
        self.multi_scroll = ctk.CTkScrollableFrame(plot_frame, height=80)
        self.multi_scroll.pack(fill="x", padx=5, pady=(0,5))

        self.multi_outs = {}


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
        for var in self.model_description.modelVariables:
            if var.causality == "parameter":
                frame = ctk.CTkFrame(self.parameter_scroll)
                frame.pack(fill="x", pady=5, padx=5)

                label = ctk.CTkLabel(frame, text=f"{var.name} ({var.type})")
                label.pack(side="left", padx=5)

                entry = ctk.CTkEntry(frame, justify="right", width=80)
                entry.pack(side="right", padx=5)
                #value_txt = str(var.start[:7]) 
                entry.insert(0, str(var.start) if var.start is not None else "0")


                self.parameter_entries[var.name] = entry



    # FMU LADEN UND PARAMETER FELDER ERSTELLEN
   
    def on_open(self): #gekürzt weil neue load funktion
        path = filedialog.askopenfilename(title="FMU Datei laden", filetypes=[("FMU Dateien", "*.fmu")])
        
        if not path:
            return 0

        self.load_fmu(path)
       

    def update_plot_dropdowns(self):
        #x-achse mit time als default
        x_values = ["time"] + (self.outputs)
        self.x_dropdown.configure(values=x_values)
        self.x_var.set("time")

        #y-achse nur outputs
        if self.outputs:
            self.y_dropdown.configure(values=["none"] + self.outputs)
            self.y_var.set(self.outputs[0])
        else:
            y_values = []
            self.y_dropdown.configure(values=y_values)
            self.y_var.set(y_values)

        #y2-achse nur outputs
        if self.outputs:
            self.y2_dropdown.configure(values=["none"] + self.outputs)
            self.y2_var.set("none")  #defaulkt wert
        else:
            y2_values = []
            self.y2_dropdown.configure(values=y2_values)
            self.y2_var.set(y2_values)




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
    
        if self.ax2 is not None:        
            self.ax2.remove()   # twinx "clear"
            self.ax2 = None


        x_name = self.x_var.get()
        y_name = self.y_var.get()
        y2_name = self.y2_var.get()

        selected = []

        if y_name != "none":
            selected.append(y_name)

        for output, var in self.multi_outs.items():
            if var.get():
                selected.append(output)
        
        if selected:
            for output in selected:
                if output in result.dtype.names:
                    self.ax.plot(result[x_name], result[output], label=output)

            self.ax.set_title("Simulationsergebnisse")
            self.ax.set_xlabel(x_name)
            self.ax.set_ylabel("|".join(selected))
            self.ax.grid(True)
        else:
            self.ax.set_title("kein y")
            self.ax.set_xlabel(x_name)
            self.ax.set_ylabel("none")
            self.ax.grid(True)

        if y2_name != "none":
            self.ax2 = self.ax.twinx()
            self.ax2.plot(result[x_name], result[y2_name], color="orange")
            
            self.ax2.set_ylabel(y2_name)
            self.ax.grid(True)


        self.canvas.draw()

        self.status.set("Simulation abgeschlossen.")

    
    def on_quick_select(self, answer): 
        if answer in self.quick_fmus:

            self.load_fmu(self.quick_fmus[answer])
 
    
    def load_fmu(self, path): # neue eigene lade-funktion
        self.fmu_path = path
        self.model_description = read_model_description(self.fmu_path)

        #outputs aus FMU lesen für dropdowns
        self.outputs = [var.name for var in self.model_description.modelVariables if var.causality == "output"]
        self.update_plot_dropdowns()
        self.create_parameter_fields()
        self.build_multi_checkboxes()

        #statusupdate
        self.status.set(f"Geladene FMU: {self.fmu_path}")

        self.y_change()

        

    #dropdown von y2 deaktivieren wenn y1 none ist    
    def y_change(self, *args):
        y_name = self.y_var.get()
        chkbx_any = any(var.get() for var in self.multi_outs.values()) 

        if y_name == "none" and not chkbx_any:
            self.y2_var.set("none")
            self.y2_dropdown.configure(state="disabled")
        else:
            self.y2_dropdown.configure(state="normal")

    # checkboxen für mehrere outputs erstellen
    def build_multi_checkboxes(self):
        #vorherige widgets löschen
        for widget in self.multi_scroll.winfo_children():
            widget.destroy()
        self.multi_outs.clear()

        for output in self.outputs:
            var = ctk.BooleanVar(value=False)
            chkbx = ctk.CTkCheckBox(self.multi_scroll, text=output, variable=var, command=self.y_change)
            chkbx.pack(anchor="w", padx=5, pady=2)

            self.multi_outs[output] = var
        
