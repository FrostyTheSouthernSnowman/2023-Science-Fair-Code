import plotly.express as px
import pandas as pd

df = pd.read_csv("max_amps.csv")

plt = px.scatter_3d(df, x='Turns', y='Diameter (Millimeters)', z='Current (Amps)')

plt.show()