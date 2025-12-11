from fmpy import read_model_description

md = read_model_description('RC_Filter.fmu')

for v in md.modelVariables:
    print(v.name, v.valueReference, v.type)
