"""
Graph variables (x is included, c is excluded)
- [x] Current (Amps)
- [c] Coil Diameter (Millimeters)
- [c] Wire Diameter,
- [c] Distance (Millimeters)
- [x] Turns,
- [c] Voltage,
- [x] Force (Newtons)
"""


import pandas as pd
import plotly.express as px
import os

path = os.path.join(os.path.dirname(__file__), '../data/9v_output.csv')

print("Reading data")
df = pd.read_csv(path)

coil_diameter = 25
wire_diameter = 5
distance = 10

print("Filtering unneeded variables")
df = df[(df["Coil Diameter (Millimeters)"] == coil_diameter) &
        (df["Wire Diameter"] == wire_diameter) &
        (df["Distance (Millimeters)"] == distance)]

fig_3d = px.scatter_3d(df, x='Current (Amps)', y='Turns', z='Force (Newtons)')
fig_2d = px.scatter(df, x='Current (Amps)', y='Turns', color='Force (Newtons)')
fig_2d.update_layout(
    title=dict(
        text="How Current and Wire Turns Affect Electromagnet Force",
        font=dict(size=24),
        x=0.5
    ),
    legend=dict(
        font=dict(size=18),
        title_font_size=20
    ),
    font=dict(size=16))

fig_3d.show()
fig_2d.show()
