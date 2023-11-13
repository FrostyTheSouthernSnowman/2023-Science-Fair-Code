"""
Graph variables (x is included, c is excluded)
- [c] Current (Amps)
- [c] Coil Diameter (Millimeters)
- [c] Wire Diameter,
- [x] Distance (Millimeters)
- [c] Turns,
- [c] Voltage,
- [x] Force (Newtons)
"""

import pandas as pd
import plotly.express as px
import os

path = os.path.join(os.path.dirname(__file__), '../data/9v_output.csv')

print("Reading data")
df = pd.read_csv(path)

current = 321
coil_diameter = 25
wire_diameter = 5
turns = 150

print("Filtering unneeded variables")
df = df[(df["Current (Amps)"] == current) &
        (df["Coil Diameter (Millimeters)"] == coil_diameter) &
        (df["Wire Diameter"] == wire_diameter) &
        (df["Turns"] == turns)]

fig = px.line(df, x='Distance (Millimeters)', y='Force (Newtons)')
fig.update_layout(
    title=dict(
        text='Force Exerted by an Electromagnet as an Object Gets Further Away',
        font=dict(size=24),
        x=0.5
    ),
    legend=dict(
        font=dict(size=18),
        title_font_size=20
    ),
    font=dict(size=16))

fig.show()
