import json
from datetime import timedelta, timezone
from pathlib import Path

import altair as alt
import pandas as pd
import pydeck as pdk
import streamlit as st
from pydeck.types import String

st.set_page_config(layout="wide")

# DEFAULT
SENSORS = [21, 25, 27, 28]
TXPOWERS = [5, 10, 15, 20, 25, 30]
TIMEZONE = timezone(-timedelta(hours=4))
# current dir
DIR = Path(".").absolute().joinpath("rssi_relative_change_WPB")


@st.cache(allow_output_mutation=True)
def prep_data(plot_data_path: Path):
    df = pd.read_csv(plot_data_path)
    df.plot_timestamp = pd.to_datetime(df.plot_timestamp)
    df.color = df.color.apply(json.loads)  # from str to list
    df.emitter = df.emitter.apply(str)  # from int to str
    df.sensor = df.sensor.apply(str)  # from int to str
    timestamps = df.plot_timestamp.unique()
    return df, timestamps


def plot_arc(
    df,
    time,
    txpower: int,
    lat_view: float = 26.713389,
    lng_view: float = -80.053782,
):
    # prepare data snapshot at a specific time point for a specific txpower
    plot_df = df[(df.plot_timestamp == time) & (df.txpower == txpower)]
    arc_layer = pdk.Layer(
        "ArcLayer",
        data=plot_df,
        get_width="width",
        get_source_position=["lng_emit", "lat_emit"],
        get_target_position=["lng_sensor", "lat_sensor"],
        get_tilt=15,
        get_source_color="color",
        get_target_color="color",
        pickable=True,
        auto_highlight=True,
    )
    emitter_id_layer = pdk.Layer(
        "TextLayer",
        data=plot_df,
        get_position=["lng_emit", "lat_emit"],
        get_text="emitter",
        get_size=50,
        get_color="color",
        get_text_anchor=String("end"),
        get_alignment_baseline=String("top"),
    )
    sensor_id_layer = pdk.Layer(
        "TextLayer",
        data=plot_df,
        get_position=["lng_sensor", "lat_sensor"],
        get_text="sensor",
        get_size=50,
        get_color=[77, 77, 255],
        get_text_anchor=String("end"),
        get_alignment_baseline=String("top"),
    )
    view_state = pdk.ViewState(
        latitude=lat_view,
        longitude=lng_view,
        pitch=50,
        zoom=20,
    )
    TOOLTIP_TEXT = {"html": "RSSI relative change: {rc}"}
    return pdk.Deck(
        [arc_layer, emitter_id_layer, sensor_id_layer],
        initial_view_state=view_state,
        tooltip=TOOLTIP_TEXT,
        map_style="road",
        map_provider="mapbox",
        api_keys={"mapbox": st.secrets["MAPBOX_API_KEY"]},
    )


# Side bars
sel_sid = st.sidebar.radio("Choose a sensor", SENSORS, index=0)
sel_tx = st.sidebar.radio("Choose a txpower", TXPOWERS, index=3)

# Data
df, timestamps = prep_data(DIR.joinpath(f"data/plot_{sel_sid}.csv"))

# Side bar slider
sel_time = st.sidebar.slider(
    "Choose a time point",
    timestamps.min().to_pydatetime(),
    timestamps.max().to_pydatetime(),
    step=timedelta(minutes=15),
    format="YYYY-MM-DD HH:mm",
)

# Main display
st.title("RSSI Relative Change Overtime - WPB - Calibration")
st.write(f"## Sniffing Sensor = S{sel_sid}")
st.write("Drag the slider on the left to view RSSI relative change ovetime.")

# Line plot
st.altair_chart(
    alt.Chart(df[(df.plot_timestamp <= sel_time) & (df.txpower == sel_tx)])
    .properties(
        width=700,
        height=400,
    )
    .mark_line()
    .encode(
        x=alt.X(
            "yearmonthdatehoursminutes(plot_timestamp)",
            type="temporal",
            axis=alt.Axis(labelAngle=-20, title="Time"),
            scale=alt.Scale(domain=[timestamps.min(), timestamps.max()]),
        ),
        y=alt.Y(
            "rc",
            axis=alt.Axis(format="%", title="Relative Change"),
            type="quantitative",
            scale=alt.Scale(domain=[-0.20, 0.40]),
        ),
        color=alt.Color("emitter", type="nominal"),
        tooltip=alt.Tooltip(["rc"]),
    ),
    use_container_width=True,
)

# Arc Plot
st.write("More positive RSSI relative change => thicker and brighter arc")
st.pydeck_chart(
    plot_arc(
        df,
        # NOTE: this time is different from the selected time. It aligns with
        # the actual time available in timestamps. The selected time is just
        # a decoy.
        sel_time,
        sel_tx,
    ),
    use_container_width=True,
)

# Display table
st.write("### Data Table")
st.write(
    df[(df.plot_timestamp == sel_time) & (df.txpower == sel_tx)].loc[
        :, ["emitter", "rssi", "rc"]
    ],
)
