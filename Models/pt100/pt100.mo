model pt100
  MT.Sensoren.PT100 pt100 annotation(
    Placement(transformation(origin = {-38, 52}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Thermal.HeatTransfer.Celsius.PrescribedTemperature prescribedTemperature annotation(
    Placement(transformation(origin = {-86, 10}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Sources.ConstantCurrent constantCurrent annotation(
    Placement(transformation(origin = {-8, -26}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Basic.Resistor resistor annotation(
    Placement(transformation(origin = {-24, 8}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Basic.Ground ground annotation(
    Placement(transformation(origin = {18, 34}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Sources.RampVoltage rampVoltage(V = 5, duration = 1, offset = 0) annotation(
    Placement(transformation(origin = {10, 110}, extent = {{10, -10}, {-10, 10}}, rotation = 90)));
equation

annotation(
    uses(Modelica(version = "3.2.3")));
end pt100;