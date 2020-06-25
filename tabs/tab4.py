import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import datetime, date, time
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import sqlalchemy as db
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app, connection_string


layout = html.Div(children=[
    html.Div([], className='test_tab4'),
], className='tabs_main_div')