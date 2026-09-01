# Messtechnik FMU Simulator

A desktop simulation environment for FMU models, developed for the course *Grundlagen der
elektronischen Messtechnik* at TU Berlin (Fachgebiet Elektronische Mess- und Diagnosetechnik).
Students load a model, change physical parameters, run the simulation and see the result
plotted — without installing a Modelica toolchain.

Team project, 6 ECTS: Yessmine Chabchoub, Simon Costamagna, Christoph Emons, David Maric.

## Features

- Loads FMU models and reads out their parameters and output signals
- Physical parameters (R, C, U, …) and simulation duration editable from the GUI
- Simulation via `fmpy`, results plotted with matplotlib
- Second tab showing the model's circuit diagram alongside the plot
- One or two independently scaled y-axes, or several outputs on one axis
- Input validation and exception handling, so a bad parameter never crashes the GUI
- Quick-select dropdown for the preloaded course models

## Included models

| Model | Topic |
| --- | --- |
| `ADU_IDEAL` | Ideal ADC characteristic |
| `ADU_Non_Ideal` | ADC characteristic with DNL and INL |
| `Messbruecke` | Measurement bridge for passive component values |
| `Leistungsmessung_Dimmer` | Power measurement on an AC dimmer, resistive load |

## Repository layout

```
GUI/                       Python application (main_gui.py, gui.py)
FMUs/                      exported FMUs and their circuit diagrams
Models/                    OpenModelica source models
Modelica Bibliothek/       Modelica library components used by the models
Templates und Beispiele/   templates and reference examples
Organisation/              project planning and documentation
SimuGEM.zip                packaged release
```

## Getting started

Python 3.11.4 is recommended — currently the best compatibility with the dependencies.

```bash
pip install pillow customtkinter matplotlib fmpy
cd GUI
python main_gui.py
```

### Note for Ubuntu

On Ubuntu 22.04 the system Python may be built without Tk support, which the GUI needs.
Install the dependencies and rebuild your Python version first:

```bash
sudo apt update
sudo apt install -y tk-dev libsqlite3-dev
```

## How it works

Models are built in OpenModelica using the Modelica Standard Library and exported as
**Model Exchange** FMUs, with the ODE solver running in Python through `fmpy`. CoSimulation
FMUs also work — the type is read when the FMU is loaded.

Only values declared as `parameter` in Modelica are surfaced in the GUI. Without that filter an
FMU exposes its entire internal variable list; this keeps the parameter panel to the physically
meaningful values.

### Cross-platform FMUs

OpenModelica FMUs contain pre-compiled binaries, so an FMU built on Linux will not run on
Windows and vice versa. Since every student on the course had to be able to run the tool, there
were two options: switch to a commercial Modelica tool that exports platform-independent FMUs,
or export each model twice and select the right one at runtime.

We chose the second. The application reads `platform.system()` at startup and expects this
naming convention in `FMUs/`:

```
<model_name>_<win|linux>.fmu
<model_name>_<win|linux>.png
```

Compatibility is checked again on load, by unpacking the FMU and verifying that its `binaries`
folder matches the host OS.

## Adding a model

1. Build the model in OpenModelica, declaring adjustable values as `parameter`
2. Define the output signals to be plotted
3. Export as Model Exchange FMU — once on Linux, once on Windows
4. Name both files per the convention above and place them in `FMUs/`
5. Optionally add the model to the quick-select dictionary in the class initialisation

## Built with

Python · CustomTkinter · matplotlib · fmpy · OpenModelica · Modelica Standard Library · FMI
