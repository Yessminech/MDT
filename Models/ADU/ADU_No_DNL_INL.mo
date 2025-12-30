model ADU_Non_Ideal
  MT.Digitalisierung.ADU adu annotation(
    Placement(transformation(origin = {10, -2}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.Ramp ramp(height = 5, duration = 1)  annotation(
    Placement(transformation(origin = {-58, -2}, extent = {{-10, -10}, {10, 10}})));
equation
  connect(adu.real_i, ramp.y) annotation(
    Line(points = {{0, -2}, {-46, -2}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "3.2.3")));
end ADU_Non_Ideal;