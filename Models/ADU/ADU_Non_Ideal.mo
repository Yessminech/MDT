model ADU_Non_Ideal
  MT.Digitalisierung.ADU adu annotation(
    Placement(transformation(origin = {6, -2}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.Ramp ramp(height = 5, duration = 1)  annotation(
    Placement(transformation(origin = {-58, -2}, extent = {{-10, -10}, {10, 10}})));
  MT.Digitalisierung.DAU dau(Umax = 5, Umin = 0, steps = 256)  annotation(
    Placement(transformation(origin = {42, -2}, extent = {{-10, -10}, {10, 10}})));
equation
  connect(adu.real_i, ramp.y) annotation(
    Line(points = {{-5, -2}, {-46, -2}}, color = {0, 0, 127}));
  connect(dau.int_i, adu.int_o) annotation(
    Line(points = {{32, -2}, {18, -2}}, color = {255, 127, 0}));
  annotation(
    uses(Modelica(version = "3.2.3")));
end ADU_Non_Ideal;