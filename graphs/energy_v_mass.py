import pandas as pd
import plotly.express as px
import os

pd.options.plotting.backend = "plotly"

em_path = os.path.join(os.path.dirname(__file__), "..",
                       "data", "mass_v_energy.csv")
m_path = os.path.join(os.path.dirname(__file__), "..",
                      "data", "motor_energy_v_mass.csv")

em_df = pd.read_csv(em_path)
m_df = pd.read_csv(m_path)
df = pd.merge(em_df, m_df, on="Mass (kg)", how="inner")
df = df.rename(columns={"Energy (J)_x": "Electromagnet Energy Consumption",
               "Energy (J)_y": "Motor Energy Consumption"})
fig = df.plot(x="Mass (kg)", y=[
              "Electromagnet Energy Consumption", "Motor Energy Consumption"])

fig.update_layout(
    title=dict(
        text="Energy Consumption to Move an Object in Space",
        font=dict(size=24),
        x=0.2
    ),
    legend=dict(
        font=dict(size=18),
        title_font_size=20
    ),
    yaxis_title="Energy Consumption (J)",
    font=dict(size=16))

fig.show()
