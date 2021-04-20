from pathlib import Path
from typing import Dict

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

# DEFAULT
SENSORS = ["s1", "s2", "s3", "s4"]
SENSOR_LOC = np.array([(0, 16), (16, 16), (0, 0), (16, 0)])
INACTIVE_COLOR = "#e6e6e6"
# current dir
DIR = Path(".").absolute().joinpath("rssi_relative_change_overtime")


# All relative change data frames
all_plot_df: Dict = {
    s: pd.read_csv(f"{DIR}/data/streamlit_demo_{s}.csv") for s in SENSORS
}
sensor_points_loc_df = pd.DataFrame.from_dict(
    {"sensor": SENSORS, "x": SENSOR_LOC[:, 0], "y": SENSOR_LOC[:, 1]},
)

# Side bars
sel_sensor = st.sidebar.radio("Choose a sensor", SENSORS, index=0)

# Main display
st.title("Localization Data Relative Change")
st.write(f"## Line Plot -- Sensor {sel_sensor[1]}")
st.write(
    """Click data collection point to view its relative change over time.
    Hold shift to select multiple points.""",
)

# Plot
target_df = all_plot_df[sel_sensor]  # data of the selected sensor
# selection_multi allows selecting multiple data_col_point
selector = alt.selection_multi(empty="none", fields=["data_col_point"])
# The plot that needs interaction must be extended from the base
base = (
    alt.Chart(target_df)
    .properties(width=350, height=350)
    .add_selection(
        selector,
    )
)
# Plot data collection point location
data_col_points = base.mark_point(filled=True, size=300).encode(
    alt.X("x", type="quantitative", axis=None),
    alt.Y("y", type="quantitative", axis=None),
    color=alt.condition(
        selector,
        "data_col_point:N",
        alt.value(INACTIVE_COLOR),
    ),
)
# Add data collection point text
data_col_text = (
    alt.Chart(target_df)
    .mark_text(dx=20, fontSize=15)
    .encode(
        x=alt.X("x", type="quantitative"),
        y=alt.Y("y", type="quantitative"),
        text=alt.Text("data_col_point:N"),
        color=alt.condition(
            selector,
            "data_col_point:N",
            alt.value(INACTIVE_COLOR),
        ),
    )
)

# Plot the sensor location. Only the selected sensor is shown.
sensor_points = (
    alt.Chart(
        sensor_points_loc_df[sensor_points_loc_df.sensor == sel_sensor],
    )
    .mark_point(filled=True, size=300, shape="diamond")
    .encode(
        x=alt.X("x", type="quantitative"),
        y=alt.Y("y", type="quantitative"),
        text=alt.Text("sensor:N"),
        color=alt.value("red"),
    )
)
# Add sensor text
sensor_text = (
    alt.Chart(
        sensor_points_loc_df[sensor_points_loc_df.sensor == sel_sensor],
    )
    .mark_text(dx=20, fontSize=15)
    .encode(
        x=alt.X("x", type="quantitative"),
        y=alt.Y("y", type="quantitative"),
        text=alt.Text("sensor:N"),
        color=alt.value("red"),
    )
)

# Plot the relative change
rlt_chng = (
    base.mark_line()
    .encode(
        x=alt.X(
            "date",
            type="nominal",
            axis=alt.Axis(labelAngle=0, title="Date"),
        ),
        y=alt.Y(
            "rc",
            axis=alt.Axis(format="%", title="Relative Change"),
            type="quantitative",
            scale=alt.Scale(domain=[-0.15, 0.15]),
        ),
        color=alt.Color(
            "data_col_point:N",
            type="nominal",
            legend=None,
        ),
        tooltip=alt.Tooltip(["rc", "data_col_point"]),
    )
    .transform_filter(selector)
)


st.altair_chart(
    rlt_chng | data_col_points + data_col_text + sensor_points + sensor_text,
    use_container_width=True,
)
