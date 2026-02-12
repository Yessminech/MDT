
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

-checkbox für alle Signale einfügen [done] by david
-modelExchange statt coSimulation standardmässig nutzen [done] by david

-erstellen eines weiteren Tabs für den passenden Schaltplan der fmu [done] by Christoph
-hinzufügen einer Auswahlmöglichkeit der anzuzeigenden Variabeln 
-Voreinstellbare Anzeigevariabeln speichern können
-Umgang mit Fehlerhaften fmu Dateien
-Sinnvolle Ausgabe von Fehlermeldungen

"""

import customtkinter as ctk
from tkinter import filedialog
from fmpy import read_model_description, simulate_fmu
from PIL import Image
import logging
import platform
from fmpy import extract
from fmpy.model_description import ModelDescription
from fmpy.fmi1 import FMICallException
import os

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


ctk.set_appearance_mode("dark")   # optionen: light, system, dark
ctk.set_default_color_theme("green")  # optionen: dark-blue, green, etc.
logging.getLogger("fmpy").setLevel(logging.ERROR) # Unterdrückt verwirrende fmpy Konsolenmeldungen


class BaseGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Betriebssystem merken
        raw_system = platform.system().lower()

        if raw_system == "windows":
            self.os_tag = "win"
        elif raw_system == "linux":
            self.os_tag = "linux"
        else:
            self.os_tag = raw_system   

        # Fenster config 
        self.title("GEM Simulationen")
        self.geometry("1000x700")
        self.minsize(900, 500)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        #schnellauswahl für vorausgewählte FMUs (Name : Dateiname)
        self.quick_fmus = {
            "WienBruecke": "WienBruecke",
            "Leistungsmessung": "Leistungsmessung",
            "Ideale_ADU": "ADU_IDEAL",
            "(Fixed)Ideale_ADU": "(FIXED)ADU_IDEAL",
            "nicht_Ideale_ADU": "ADU_Non_Ideal"
        }

        # GUI Komponenten erstellen
        self.create_topbar()
        self.create_left_panel()
        self.create_tabs()
        self.create_statusbar()

        self.fmu_path = None  #Pfad zur geladenen FMU
        self.last_result = None  #Simulationsergebnisse
        self.model_description = None
        
        self.default_entry_border = ctk.ThemeManager.theme["CTkEntry"]["border_color"]  #standart Borderfarbe

        self.ax2 = None #zweite y-Achse
        
    def is_plottable(self, var):
        #nur Real
        if getattr(var, "type", None) != "Real":
            return False

        name = var.name
        causality = getattr(var, "causality", None)
        variability = getattr(var, "variability", None)
        unit = getattr(var, "unit", None)

        #harte Ausschlüsse
        if name.startswith("der("):
            return False
        if variability == "parameter":
            return False

        #Einheiten
        if name.endswith((".v", ".i", ".y", ".u")):
            return True
        if unit in ("V", "A"):
            return True

        #übrige (okaye )Kandidaten
        if causality in ("output", "calculatedParameter", None):
            return True

        return False




    
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

        #checkbox zum zeigen von allen parametern
        self.show_all_var = ctk.BooleanVar(value = False)
        self.show_all_checkbox = ctk.CTkCheckBox(plot_frame, text = "alle Signale ON/OFF", variable = self.show_all_var, command = self.update_plot_dropdowns)
        self.show_all_checkbox.pack(anchor = "w", padx = 5, pady = (0, 4))

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
    def create_tabs(self):
        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Tabs anlegen
        self.sim_tab = self.tabs.add("Simulation")
        self.image_tab = self.tabs.add("FMU Ansicht")

        # Grid config
        self.sim_tab.grid_rowconfigure(0, weight=1)
        self.sim_tab.grid_columnconfigure(0, weight=1)

        self.image_tab.grid_rowconfigure(0, weight=1)
        self.image_tab.grid_columnconfigure(0, weight=1)

        # Inhalte erzeugen
        self.create_main_view()
        self.create_image_view()

    
    def create_main_view(self):
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Simulation")
        self.ax.set_xlabel("Zeit")
        self.ax.set_ylabel("Wert")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.sim_tab)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


    def create_image_view(self):
        #weißer Hintergund
        self.image_container = ctk.CTkFrame(
            self.image_tab,
            fg_color="white"
        )
        self.image_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.image_container.grid_rowconfigure(0, weight=1)
        self.image_container.grid_columnconfigure(0, weight=1)

        self.image_label = ctk.CTkLabel(
            self.image_container,
            text="Keine FMU geladen",
            anchor="center",
            text_color="black"
        )
        self.image_label.image = None
        self.image_label.grid(row=0, column=0, sticky="nsew")


    def get_os_specific_fmu(self, base_name):
        filename = f"{base_name}_{self.os_tag}.fmu"
        return os.path.join("FMUs", filename)


    def load_fmu_image(self, fmu_path):
        self.image_label.configure(text="Lade Bild...")
        self.image_label.image = None

        if hasattr(self, "fmu_image"):#Löscht alte Bildreferenz
            del self.fmu_image


        base, _ = os.path.splitext(fmu_path)
        img_path = base + ".png"

        if not os.path.exists(img_path):
            self.image_label.configure(text="Kein PNG zur FMU gefunden")
            return

        # Originalbild laden
        img = Image.open(img_path)

        # Layout aktualisieren
        self.update_idletasks()

        tab_w = self.image_container.winfo_width()
        tab_h = self.image_container.winfo_height()

        # Fallback
        if tab_w <= 1 or tab_h <= 1:
            tab_w, tab_h = 800, 600

        max_w = int(tab_w * 0.8)
        max_h = int(tab_h * 0.8)

        # Standard: Originalgröße
        new_w, new_h = img.width, img.height

        # NUR skalieren, wenn Bild zu groß ist
        if img.width > max_w or img.height > max_h:

            img_ratio = img.width / img.height
            container_ratio = max_w / max_h

            if img_ratio > container_ratio:
                new_w = max_w
                new_h = int(max_w / img_ratio)
            else:
                new_h = max_h
                new_w = int(max_h * img_ratio)

            img = img.resize((new_w, new_h), Image.LANCZOS)

        self.fmu_image = ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(new_w, new_h)
        )

        self.image_label.configure(text="", image=self.fmu_image)
        self.image_label.image = self.fmu_image  # Referenz halten






    
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

                entry.configure(border_width=1, border_color=self.default_entry_border)

                self.parameter_entries[var.name] = entry



    # FMU LADEN UND PARAMETER FELDER ERSTELLEN
   
    def on_open(self): #gekürzt weil neue load funktion
        path = filedialog.askopenfilename(title="FMU Datei laden", filetypes=[("FMU Dateien", "*.fmu")])
        
        if not path:
            return 0

        self.load_fmu(path)
       

    def update_plot_dropdowns(self):

        if getattr(self, "show_all_var", None) is not None and self.show_all_var.get():
            signals = getattr(self, "all_plottable", [])
        else:
            signals = getattr(self, "outputs", [])
        



        #x-achse mit time als default
        x_values = ["time"] + signals
        self.x_dropdown.configure(values=x_values)
        if self.x_var.get() not in x_values:
            self.x_var.set("time")

        #y-achse nur outputs

        if signals:
            self.y_dropdown.configure(values=["none"] + signals)
            if self.y_var.get() not in (["none"] + signals):
                self.y_var.set(signals[0])
        else:
            self.y_dropdown.configure(values = "none")
            self.y_var.set("none")

        #y2-achse nur outputs
        if signals:
            self.y2_dropdown.configure(values=["none"] + signals)
            if self.y2_var.get() not in (["none"] + signals):
                self.y2_var.set(signals[0])
        else:
            self.y2_dropdown.configure(values = "none")
            self.y2_var.set("none")



    #übernahme von standardwerten aus FMU für start_time, stop_time, step_size ###################### GESTRICHEN - bleibt für potenzielle Fehlerbehandlung
    def get_time_setting(self, user_stop_time: float):
        md = self.model_description

        start_time = 0.0
        stop_time = user_stop_time
        step_size = None

        desc = getattr(md, "defaultExperiment", None)
        if desc is not None:
            if getattr(desc, "startTime", None) is not None:
                start_time = float(desc.startTime)
            

        if step_size is None:
            step_size = max(stop_time / 1000.0, 1e-9)

        return start_time, stop_time, step_size





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
            user_stop_time = float(self.stop_time_entry.get())
            if user_stop_time <= 0:
                raise ValueError
        except Exception:
            self.status.set("Ungueltiger Wert für stop time.")
            return 0
        
        #start_time, stop_time, step_size holen
        start_time, stop_time, step_size = self.get_time_setting(user_stop_time)

    

        #simulieren
        self.reset_parameter_marking()

        invalid_params = self.validate_parameters()
        if invalid_params:
            for p in invalid_params:
                self.mark_parameter_invalid(p)
            self.status.set("Ungültige Parameter markiert.")
            return
        
        #cosim oder exchange?
        #fmi_type = "CoSimulation" if self.model_description.coSimulation else "ModelExchange"

        #fmu-typ wählen (diesmal das es klappt)
        md = self.model_description
        if md.modelExchange:
            fmi_type = "ModelExchange"
        else: 
            fmi_type = "CoSimulation"
        
        try:
            result = simulate_fmu(
                self.fmu_path,
                start_values=start_values,
                stop_time=stop_time,
                start_time = start_time,
                fmi_type = fmi_type
            )


        except FMICallException as e:
            self.status.set("FMU-Simulationsfehler.")
            print("FMU-Fehler:", e)
            return
        except Exception as e:
            self.status.set("Allgemeiner Simulationsfehler.")
            print("Fehler:", e)
            return
        
        
        




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

            base_name = self.quick_fmus[answer]
            fmu_path = self.get_os_specific_fmu(base_name)

            if not os.path.exists(fmu_path):
                self.status.set(f"FMU nicht gefunden: {fmu_path}")
                return

            self.load_fmu(fmu_path)

 
    #lade-funktion für fmus
    def load_fmu(self, path): 
        self.fmu_path = path
        self.model_description = read_model_description(self.fmu_path)

        issues = self.check_fmu_compatibility(path)

        if issues:
            self.status.set("FMU inkompatibel – siehe Konsole")
            for issue in issues:
                print("FMU-Warnung:", issue)

        #outputs aus FMU lesen für dropdowns
        self.outputs = [var.name for var in self.model_description.modelVariables if var.causality == "output" ]

        self.all_plottable = [var.name for var in self.model_description.modelVariables if self.is_plottable(var)]


        self.update_plot_dropdowns()
        self.create_parameter_fields()
        self.build_multi_checkboxes()

        self.load_fmu_image(path)

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
    
    #Überprüfung der fmu Binary dür windows Linux usw..
    def check_fmu_compatibility(self, fmu_path):
        issues = []

        # OS prüfen
        raw_system = platform.system().lower()

        platform_map = {
            "windows": "win",
            "linux": "linux",
            "darwin": "darwin"
        }
        system = platform_map.get(raw_system, raw_system)# windows / linux / darwin

        
        unzipdir = extract(fmu_path)
        binaries_path = os.path.join(unzipdir, "binaries")
        if not os.path.exists(binaries_path):
            issues.append("FMU enthält keine Binaries.")
            return issues

        available_platforms = os.listdir(binaries_path)
        #print(available_platforms)
        platform_ok = False
        for p in available_platforms:
            #print(p.lower())
            if system in p.lower():
                platform_ok = True

        if not platform_ok:
            issues.append(
                f"Keine passenden Binaries für {system}. Gefunden: {available_platforms}"
            )

        # FMI-Typ prüfen (angepasst)
        md = self.model_description
        if not md.coSimulation:
            issues.append("FMU unterstützt keine ModelExchange (nur CoSimulation).")
        return issues
    
    #rote Makierung von Fehlerhaften Eingabewerten
    def mark_parameter_invalid(self, name):
        entry = self.parameter_entries.get(name)
        if entry:
            entry.configure(border_color="red")
    
    #Zurücksetzen der Farbe des Eingabewertes
    def reset_parameter_marking(self):
        for entry in self.parameter_entries.values():
            entry.configure(border_color=self.default_entry_border)


    def validate_parameters(self):
        invalid = []

        for var in self.model_description.modelVariables:
            if var.causality == "parameter" and var.name in self.parameter_entries:
                entry = self.parameter_entries[var.name]
                try:
                    value = float(entry.get())
                except ValueError:
                    invalid.append(var.name)
                    continue

                # optionale FMU-Grenzen
                if var.min is not None and value < float(var.min):
                    invalid.append(var.name)
                if var.max is not None and value > float(var.max):
                    invalid.append(var.name)

        return invalid
    
