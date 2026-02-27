model Leistungsmessung_Dimmer_FMU

  import Modelica.SIunits;

  // ===== Quelle =====
  Modelica.Electrical.Analog.Sources.SineVoltage netz(
    V = 325,          // 230V RMS
    freqHz = 50)
    annotation(Placement(transformation(origin = {-80,0}, extent={{-10,-10},{10,10}})));

  // ===== Dimmer (idealer Schalter mit Zündwinkel) =====
  Modelica.Electrical.Analog.Ideal.IdealClosingSwitch dimmer
    annotation(Placement(transformation(origin = {-20,0}, extent={{-10,-10},{10,10}})));

  // ===== Ohmsche Last =====
  Modelica.Electrical.Analog.Basic.Resistor R(R = 100)
    annotation(Placement(transformation(origin = {40,0}, extent={{-10,-10},{10,10}})));

  Modelica.Electrical.Analog.Basic.Ground ground
    annotation(Placement(transformation(origin = {-80,-40}, extent={{-10,-10},{10,10}})));

  // ===== Sensoren =====
  Modelica.Electrical.Analog.Sensors.VoltageSensor voltageSensor
    annotation(Placement(transformation(origin = {70,0}, extent={{-10,-10},{10,10}})));

  // ===== Parameter =====
  parameter Real alpha_deg = 60 "Zündwinkel in Grad";
  parameter SIunits.Frequency f = 50;
  parameter SIunits.Time T = 1/f;

  // ===== Outputs (FMU sichtbar) =====
  output SIunits.Voltage u      "Momentanspannung Last";
  output SIunits.Current i      "Momentanstrom Last";
  output SIunits.Power   P      "Momentanleistung";

  output SIunits.Voltage U_rms  "Effektivspannung";
  output SIunits.Current I_rms  "Effektivstrom";
  output SIunits.Power   P_avg  "Mittlere Wirkleistung";
  output SIunits.Power   S      "Scheinleistung";
  output Real            cosphi "Leistungsfaktor";
  output Real            alpha  "Zündwinkel (Grad)";

protected 
  SIunits.Power P_int(start=0);
  Real u_sq_int(start=0);
  Real i_sq_int(start=0);

equation

  // ===== Elektrische Verschaltung =====
  connect(netz.p, dimmer.p);
  connect(dimmer.n, R.p);
  connect(R.n, ground.p);
  connect(netz.n, ground.p);

  connect(voltageSensor.p, R.p);
  connect(voltageSensor.n, R.n);

  // ===== Dimmer-Ansteuerung (Phasenanschnitt) =====
  dimmer.control = 
    if sin(2*Modelica.Constants.pi*f*time) > 
       sin(2*Modelica.Constants.pi*f*time - alpha_deg*Modelica.Constants.pi/180)
    then true else false;

  // ===== Momentanwerte =====
  u = voltageSensor.v;
  i = u / R.R;
  P = u * i;
  alpha = alpha_deg;

  // ===== Kontinuierliche Mittelwertbildung =====
  der(P_int)    = P;
  der(u_sq_int) = u^2;
  der(i_sq_int) = i^2;

  P_avg = P_int / T;
  U_rms = sqrt(u_sq_int / T);
  I_rms = sqrt(i_sq_int / T);

  S = U_rms * I_rms;
  cosphi = P_avg / S;

  annotation(
    uses(Modelica(version="3.2.3")),
    experiment(StartTime=0, StopTime=0.2, Tolerance=1e-6)
  );

end Leistungsmessung_Dimmer_FMU;
