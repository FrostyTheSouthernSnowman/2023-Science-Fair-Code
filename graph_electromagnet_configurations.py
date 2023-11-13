import pandas as pd
import plotly.express as px

pd.options.plotting.backend = "plotly" 

df = pd.read_csv('7.4V_output.csv')

fig = px.scatter_3d(df, x='Turns', y='Current (Amps)', z='Coil Diameter (Millimeters)', color="Force (Newtons)")
#fig = px.line(df, x='Turns', y='Current (Amps)')

fig.show()
