#!/usr/bin/env python
# coding: utf-8

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask

import plotly.express as px
import pandas as pd

from lib.figures import Figures

server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config.suppress_callback_exceptions = True

# Init data
figures = Figures(None, "/app/data/dashboard_data.csv")
figs, data = figures.generate_dash_plots()
app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash 2020"),
        html.Div(children="""Dash: A web application framework for Python."""),
        dcc.Graph(
            id='example-graph',
            figure=figs["tree_map"]
        ),
    ]
)

if __name__ == "__main__":
    import os
    debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
    app.run_server(host="0.0.0.0", port=8050, debug=debug)


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
#df = pd.DataFrame({
#    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#    "Amount": [4, 1, 2, 2, 4, 5],
#    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
#})

#fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

#fig = figs[0]

#app.layout = html.Div(children=[
#    html.H1(children='Hello Dash'),

#    html.Div(children='''
#        Dash: A web application framework for Python.
#    '''),

#    dcc.Graph(
#        id='example-graph',
#        figure=fig
#    )
#])

#if __name__ == "__main__":
#    import os
#
#    debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
#    app.run_server(host="0.0.0.0", port=8050, debug=debug)