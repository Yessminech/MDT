model ADU_Non_Ideal
  MT.Digitalisierung.ADU adu annotation(
    Placement(transformation(origin = {6, -2}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.Ramp ramp(height = 5, duration = 1)  annotation(
    Placement(transformation(origin = {-84, -2}, extent = {{-10, -10}, {10, 10}})));
  MT.Digitalisierung.DAU dau(Umax = 5, Umin = 0, steps = 256)  annotation(
    Placement(transformation(origin = {42, -2}, extent = {{-10, -10}, {10, 10}})));
  MT.Math.GaussianNoise gaussianNoise(sigma = 0.00195)  annotation(
    Placement(transformation(origin = {-84, 28}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Add add annotation(
    Placement(transformation(origin = {-24, -2}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealOutput u annotation(
    Placement(transformation(origin = {-2, -44}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {36, 110}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealOutput y annotation(
    Placement(transformation(origin = {80, -16}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {38, 82}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.IntegerOutput yInt annotation(
    Placement(transformation(origin = {80, -40}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {38, 58}, extent = {{-10, -10}, {10, 10}})));
equation
  connect(dau.int_i, adu.int_o) annotation(
    Line(points = {{32, -2}, {18, -2}}, color = {255, 127, 0}));
  connect(gaussianNoise.y, add.u1) annotation(
    Line(points = {{-72, 28}, {-36, 28}, {-36, 4}}, color = {0, 0, 127}));
  connect(ramp.y, add.u2) annotation(
    Line(points = {{-72, -2}, {-54, -2}, {-54, -8}, {-36, -8}}, color = {0, 0, 127}));
  connect(adu.real_i, add.y) annotation(
    Line(points = {{-4, -2}, {-12, -2}}, color = {0, 0, 127}));
  connect(ramp.y, u) annotation(
    Line(points = {{-72, -2}, {-54, -2}, {-54, -44}, {-2, -44}}, color = {0, 0, 127}));
  connect(dau.real_o, y) annotation(
    Line(points = {{54, -2}, {64, -2}, {64, -16}, {80, -16}}, color = {0, 0, 127}));
  connect(adu.int_o, yInt) annotation(
    Line(points = {{18, -2}, {20, -2}, {20, -40}, {80, -40}}, color = {255, 127, 0}));
  annotation(
    uses(Modelica(version = "3.2.3")));
end ADU_Non_Ideal;