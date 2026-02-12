model ADU_IDEAL
  MT.Digitalisierung.ADUideal aDUideal(uMax = 5, uMin = 0) annotation(
    Placement(transformation(origin = {12, 0}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Sources.RampVoltage rampVoltage(V = 5, duration = 1, offset = 0) annotation(
    Placement(transformation(origin = {-56, 4}, extent = {{10, -10}, {-10, 10}}, rotation = 90)));
  Modelica.Electrical.Analog.Basic.Ground ground annotation(
    Placement(transformation(origin = {-56, -36}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealOutput u annotation(
    Placement(transformation(origin = {86, 44}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {58, 6}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealOutput y annotation(
    Placement(transformation(origin = {84, 0}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {60, -22}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.IntegerOutput yInt annotation(
    Placement(transformation(origin = {60, -20}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {60, -46}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Sensors.VoltageSensor voltageSensor annotation(
    Placement(transformation(origin = {-82, 4}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
equation
  connect(aDUideal.pin_n, rampVoltage.n) annotation(
    Line(points = {{2, -6}, {-56, -6}}, color = {0, 0, 255}));
  connect(aDUideal.pin_p, rampVoltage.p) annotation(
    Line(points = {{2, 6}, {-33, 6}, {-33, 14}, {-56, 14}}, color = {0, 0, 255}));
  connect(ground.p, rampVoltage.n) annotation(
    Line(points = {{-56, -26}, {-56, -6}}, color = {0, 0, 255}));
  connect(aDUideal.yInteger, yInt) annotation(
    Line(points = {{24, -6}, {60, -6}, {60, -20}}, color = {255, 127, 0}));
  connect(aDUideal.y, y) annotation(
    Line(points = {{24, 0}, {84, 0}}, color = {0, 0, 127}));
  connect(rampVoltage.n, voltageSensor.n) annotation(
    Line(points = {{-56, -6}, {-82, -6}}, color = {0, 0, 255}));
  connect(rampVoltage.p, voltageSensor.p) annotation(
    Line(points = {{-56, 14}, {-82, 14}}, color = {0, 0, 255}));
  connect(voltageSensor.v, u) annotation(
    Line(points = {{-93, 4}, {-97.219, 4}, {-97.219, 44}, {86, 44}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "3.2.3")));
end ADU_IDEAL;