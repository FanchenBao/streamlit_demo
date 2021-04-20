# Description
At the moment, this is a toy project to help me learn [Streamlit](https://streamlit.io/). Streamlit, along with the magic in [Altair](https://altair-viz.github.io/), offers a simple set of tools to spin up a web app for feature-rich interactive data visualization. I recommend everyone interested in data science to get your hands dirty with Streamlit. Although the tool is still in its early stage and there are key features currently not well supported (e.g. click on the map and get the data back to Python, but according to [this article](https://dev.to/andfanilo/streamlit-components-scatterplot-with-selection-using-plotly-js-3d7n), it seems to be possible to achieve this already), I see huge potential in it.

# Directory Layout
The current organization of this repo is that each individual app lives in its own folder, which contains the Python script that Streamlit runs and the data.

## rssi_relative_change_overtime
This app is my first attempt at using Streamlit. It aims to offer an interactive view of RSSI drift overtime at different data collection locations. If this does not make any sense, that is fine. The sole purpose of this app is for practice and offer me an easy-to-use interface for some data exploration.

_Checkout the app [here]()._