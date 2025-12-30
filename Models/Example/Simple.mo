model Simple
  Modelica.Blocks.Sources.Sine sine1;
  Modelica.Blocks.Continuous.FirstOrder firstorder1;
equation
  connect(sine1.y,firstorder1.u);
end Simple;
