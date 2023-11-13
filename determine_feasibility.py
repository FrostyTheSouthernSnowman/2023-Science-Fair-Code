import pandas as pd
import plotly.express as px

df = pd.read_csv("7.4V_output.csv")

df = df[df["Distance (Millimeters)"] == 10]
df = df[df["Current (Amps)"] <= 3]
#df = df[df["Wire Diameter"] <= 3]
#df = df[df["Coil Diameter (Millimeters)"] >= 10]

print(df.head())

df = df[::1000]

fig = px.scatter_3d(df, x='Coil Diameter (Millimeters)', y='Wire Diameter', z='Turns', color='Current (Amps)')

fig.show()