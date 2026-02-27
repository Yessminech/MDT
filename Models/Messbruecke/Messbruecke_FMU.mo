model Messbruecke_FMU

  import Modelica.SIunits;

  // ===== Quelle =====
  Modelica.Electrical.Analog.Sources.SineVoltage source(
    V = 10,
    freqHz = 1000)
    annotation (Placement(transformation(extent={{-80,20},{-60,40}})));

  Modelica.Electrical.Analog.Basic.Ground ground
    annotation (Placement(transformation(extent={{-80,-40},{-60,-20}})));

  // ===== Referenzzweig =====
  Modelica.Electrical.Analog.Basic.Resistor R1(R=1000)
    annotation (Placement(transformation(extent={{-20,40},{0,60}})));

  Modelica.Electrical.Analog.Basic.Capacitor C1(C=1e-6)
    annotation (Placement(transformation(extent={{-20,0},{0,20}})));

  // ===== Messzweig =====
  Modelica.Electrical.Analog.Basic.Resistor R2(R=1000)
    annotation (Placement(transformation(extent={{40,40},{60,60}})));

  Modelica.Electrical.Analog.Basic.Capacitor Cx(C=0.5e-6)
    annotation (Placement(transformation(extent={{40,0},{60,20}})));

  // ===== Differenzspannungs-Sensor =====
  Modelica.Electrical.Analog.Sensors.VoltageSensor bridgeSensor
    annotation (Placement(transformation(extent={{10,10},{30,30}})));

  // ===== Outputs für FMU =====
  output SIunits.Voltage u_source   "Quellenspannung";
  output SIunits.Voltage u_ref      "Spannung Referenzzweig";
  output SIunits.Voltage u_meas     "Spannung Messzweig";
  output SIunits.Voltage u_bridge   "Brückendifferenzspannung";

equation

  // ===== Elektrische Verschaltung =====
  connect(source.n, ground.p);

  connect(source.p, R1.p);
  connect(source.p, R2.p);

  connect(R1.n, C1.p);
  connect(C1.n, ground.p);

  connect(R2.n, Cx.p);
  connect(Cx.n, ground.p);

  connect(bridgeSensor.p, R1.n);
  connect(bridgeSensor.n, R2.n);

  // ===== Output-Zuweisungen =====
  u_source = source.v;
  u_ref    = R1.n.v;
  u_meas   = R2.n.v;
  u_bridge = bridgeSensor.v;

  annotation(
    uses(Modelica(version="3.2.3")),
    experiment(StartTime=0, StopTime=0.01, Tolerance=1e-6)
  );

end Messbruecke_FMU;
