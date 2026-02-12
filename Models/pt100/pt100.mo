model pt100
  MT.Sensoren.PT100 pt100(useHeatPort = true, R(start = 0)) annotation(
    Placement(transformation(origin = {0, -6}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  Modelica.Electrical.Analog.Sources.ConstantCurrent constantCurrent(I = 0.001) annotation(
    Placement(transformation(origin = {0, -56}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Electrical.Analog.Basic.Ground ground annotation(
    Placement(transformation(origin = {-66, -104}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Thermal.HeatTransfer.Celsius.PrescribedTemperature prescribedTemperature annotation(
    Placement(transformation(origin = {46, 4}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Blocks.Sources.Ramp ramp1(duration = 100, height = 100, offset = 0) annotation(
    Placement(transformation(origin = {-32, 32}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealOutput y1 annotation(
    Placement(transformation(origin = {72, 32}, extent = {{-10, -10}, {10, 10}}, rotation = 180), iconTransformation(origin = {38, 172}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealOutput y11 annotation(
    Placement(transformation(origin = {72, -34}, extent = {{-10, -10}, {10, 10}}, rotation = 180), iconTransformation(origin = {38, 172}, extent = {{-10, -10}, {10, 10}})));
equation
  connect(constantCurrent.n, ground.p) annotation(
    Line(points = {{0, -66}, {0, -81}, {-66, -81}, {-66, -94}}, color = {0, 0, 255}));
  connect( constantCurrent.p, pt100.PinP) annotation(
    Line(points = {{0, -46}, {0, -16}}, color = {0, 0, 255}));
  connect( prescribedTemperature.port, pt100.heatPort) annotation(
    Line(points = {{46, -6}, {10, -6}}, color = {191, 0, 0}));
  connect(ramp1.y, prescribedTemperature.T) annotation(
    Line(points = {{-21, 32}, {47, 32}, {47, 16}, {46, 16}}, color = {0, 0, 127}));
  connect(y1, ramp1.y) annotation(
    Line(points = {{72, 32}, {-21, 32}}, color = {0, 0, 127}));
  connect(ground.p, pt100.PinM) annotation(
    Line(points = {{-66, -94}, {-66, 10}, {0, 10}, {0, 4}}, color = {0, 0, 255}));
  connect(pt100.R_out, y11) annotation(
    Line(points = {{-10, -6}, {-34, -6}, {-34, -34}, {72, -34}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "3.2.3")));
end pt100;