model ADU_IDEAL
  MT.Digitalisierung.ADUideal aDUideal(uMax = 5, uMin = 0)  annotation(
    Placement(transformation(origin = {12, 0}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Sources.RampVoltage rampVoltage(V = 5, duration = 1, offset = 0)  annotation(
    Placement(transformation(origin = {-56, 0}, extent = {{10, -10}, {-10, 10}})));
  Modelica.Electrical.Analog.Basic.Ground ground annotation(
    Placement(transformation(origin = {-58, -22}, extent = {{-10, -10}, {10, 10}})));
equation
  connect(aDUideal.pin_n, rampVoltage.n) annotation(
    Line(points = {{2, -6}, {-66, -6}, {-66, 0}}, color = {0, 0, 255}));
  connect(aDUideal.pin_p, rampVoltage.p) annotation(
    Line(points = {{2, 6}, {-46, 6}, {-46, 0}}, color = {0, 0, 255}));
  connect(ground.p, rampVoltage.n) annotation(
    Line(points = {{-58, -12}, {-66, -12}, {-66, 0}}, color = {0, 0, 255}));

annotation(
    uses(Modelica(version = "3.2.3")));
end ADU_IDEAL;