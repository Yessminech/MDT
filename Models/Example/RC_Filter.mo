model RC_Filter
  Modelica.Electrical.Analog.Basic.Resistor R1(R=1000)
    annotation(Placement(transformation(extent={{-40,20},{-20,40}})));

  Modelica.Electrical.Analog.Basic.Capacitor C1(C=1e-6)
    annotation(Placement(transformation(extent={{20,20},{40,40}})));

  Modelica.Electrical.Analog.Sources.SineVoltage Vin(V=1, f=1000)
    annotation(Placement(transformation(origin = {2, 0}, extent = {{-80, 20}, {-60, 40}})));

  Modelica.Electrical.Analog.Basic.Ground G
    annotation(Placement(transformation(origin = {-30, -12}, extent = {{20, -10}, {40, 10}})));

  Modelica.Electrical.Analog.Sensors.VoltageSensor Vs
    annotation(Placement(transformation(origin = {2, -6}, extent = {{20, 60}, {40, 80}})));

equation
  connect(R1.n, C1.p);
  connect(C1.n, G.p);
  connect(Vs.p, C1.p);
  connect(Vs.n, G.p);
  connect(R1.n, C1.p) annotation(
    Line(points = {{-20, 30}, {20, 30}}, color = {0, 0, 255}));
  connect(C1.n, G.p) annotation(
    Line(points = {{40, 30}, {60, 30}, {60, -2}, {0, -2}}, color = {0, 0, 255}));
  connect(Vs.p, C1.p) annotation(
    Line(points = {{22, 64}, {20, 64}, {20, 30}}, color = {0, 0, 255}));
  connect(Vs.n, C1.n) annotation(
    Line(points = {{42, 64}, {40, 64}, {40, 30}}, color = {0, 0, 255}));
  connect(Vin.n, R1.p) annotation(
    Line(points = {{-58, 30}, {-40, 30}}, color = {0, 0, 255}));
  connect(Vin.p, G.p) annotation(
    Line(points = {{-78, 30}, {-80, 30}, {-80, -2}, {0, -2}}, color = {0, 0, 255}));

annotation(
  Icon(graphics = {
    Rectangle(extent={{-100,100},{100,-100}}, lineColor={0,0,255}),
    Text(extent={{-80,20},{80,-20}}, textString="RC Filter")
  }),

  Diagram(graphics = {Text(extent = {{-60, -60}, {60, -80}}, textString = "RC Low-Pass Filter")}));
end RC_Filter;