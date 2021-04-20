# Description
At the moment, this is a toy project to help me learn [Streamlit](https://streamlit.io/). Streamlit, along with the magic in [Altair](https://altair-viz.github.io/), offers a simple set of tools to spin up a web app for feature-rich interactive data visualization. I recommend everyone interested in data science to get your hands dirty with Streamlit. Although the tool is still in its early stage and there are key features currently not well supported (e.g. click on the map and get the data back to Python, but according to [this article](https://dev.to/andfanilo/streamlit-components-scatterplot-with-selection-using-plotly-js-3d7n), it seems to be possible to achieve this already), I see huge potential in it.

# Directory Layout
The current organization of this repo is that each individual app lives in its own folder, which contains the Python script that Streamlit runs and the data.

## rssi_relative_change_overtime ([app link](https://share.streamlit.io/fanchenbao/streamlit_demo/rssi_relative_change_overtime/app.py))
This app is my first attempt at using Streamlit. It aims to offer an interactive view of RSSI drift overtime at different data collection locations. If this does not make any sense, that is fine. The sole purpose of this app is for practice and offer me an easy-to-use interface for some data exploration.



# App Deployment Troubleshoot
Listed below are the problems I have encountered during deployment. For more community support, check out the [Streamlit forum](https://discuss.streamlit.io/)

## Install `psycopg2` on AWS EC2 Amazon Linux and Debian

As always `psycopg2` offers the most pain whenever it needs to be installed. According to its [documentation](https://www.psycopg.org/docs/install.html#build-prerequisites), the most common problems are:

1. No C compiler
2. No `Python.h` head file
3. No `pg_config` file

For Amazon Linux, the solution is to run `sudo yum install gcc python38-devel postgresql-devel` and then install `psycopg2`. Of course, `python38-devel` should change according to the Python version in use.

For Debian (the docker container used by Streamlit share is Debian), the solution is to run `sudo apt-get install gcc python3-dev libpq-dev`. Note that when we deploy the app via Streamlit share, we do not have direct access to their docker container. Therefore, according to the [documentation](https://docs.streamlit.io/en/stable/deploy_streamlit_app.html#add-or-remove-dependencies), we need to create a `packages.txt` file to list the packages we want to install.

## "Streamlit server consistently failed status checks" Error
This error happens recently on the free deployment service of Streamlit. There is a good discussion post on the forum, and I have chimed in [my findings](https://discuss.streamlit.io/t/manager-streamlit-server-consistently-failed-status-checks/11737/14?u=fanchenbao) as well. Read through the thread to find a work around for this problem.
