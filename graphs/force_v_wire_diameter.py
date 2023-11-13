"""
Graph variables (x is included, c is excluded)
- [c] Current (Amps)
- [c] Coil Diameter (Millimeters)
- [x] Wire Diameter,
- [c] Distance (Millimeters)
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

current = 349
coil_diameter = 25
distance = 10
turns = 150

print("Filtering unneeded variables")
df = df[(df["Current (Amps)"] == current) &
        (df["Coil Diameter (Millimeters)"] == coil_diameter) &
        (df["Distance (Millimeters)"] == distance) &
        (df["Turns"] == turns)]

fig = px.line(df, x='Wire Diameter', y='Force (Newtons)')

fig.update_layout(
    title=dict(
        text='Force Exerted by an Electromagnet as the Wire Used Gets Thicker',
        font=dict(size=24),
        x=0.5
    ),
    legend=dict(
        font=dict(size=18),
        title_font_size=20
    ),
    xaxis_title="Wire Diameter (Millimeters)",
    font=dict(size=16))

fig.show()
