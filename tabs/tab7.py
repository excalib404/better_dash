import dash
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



date_default = datetime.today()
start_date_default = pd.to_datetime(datetime(date_default.year, date_default.month, 1))
end_date_default = pd.to_datetime(datetime(date_default.year, date_default.month, date_default.day))


engine = create_engine(connection_string)
query = '''select time::date, name, village, building, stage, user_id 
               from "UserVillage"
               order by time, village, building, stage, user_id'''


df_buildings = pd.io.sql.read_sql(query, con=engine) \
    .rename(
    columns={'time': 'Date', 'village': 'Village', 'building': 'Building', 'stage': 'Stage', 'user_id': 'User_id'})

df_villages_default = df_buildings.loc[(df_buildings['Date'] >= start_date_default) & (df_buildings['Date'] <= end_date_default)
                                       & (df_buildings['name'] == 'village_unlocked')].drop(columns=['name', 'Building', 'Stage'])

df_villages = df_buildings.loc[(df_buildings['Date'] >= start_date_default) & (df_buildings['Date'] <= end_date_default)
                                        & (df_buildings['name'] == 'village_unlocked')].drop(columns=['name']).groupby('Village')['User_id'].nunique()

bar_color = ['#30486{0}'.format(n) for n in range(1, 9)]
def generate_bar_chart(x_data, y_data, title):
    return {
        'data': [go.Bar(x=x_data,
                        y=y_data,
                        marker=dict(color=bar_color),
                        text=y_data,
                        textposition='outside',
                        hoverinfo='y',
                        cliponaxis=False
                        )
                 ],
        'layout': go.Layout(title=title,
                            yaxis=dict(
                                showline=False,
                            ),
                            xaxis=dict(
                                showline=False,
                                dtick=1
                            )
                            )
    }

layout = html.Div(children=[
    html.Div([
        html.Div([
            html.Label('Выбор даты', className='label'),
            dcc.DatePickerSingle(id='start_date_funnel_villages', style={'float': 'left', 'height': '36px'},
                                 date = datetime(date_default.year, date_default.month, 1),
                                 placeholder='Start date',
                                 display_format='D MMMM YYYY'),

            html.Div([html.H5('-')], style={'float': 'left', 'margin-left': '5px', 'margin-right': '5px'}),
            dcc.DatePickerSingle(id='end_date_funnel_villages', className='end_date',
                                 date = datetime(date_default.year, date_default.month, date_default.day),
                                 placeholder='End date',
                                 display_format='D MMMM YYYY')

            ], className='date_select_wrapper fm_element')
        ], className='filter_menu'),

    html.Div(children=[
        html.Button('Таблица', id='table_btn', n_clicks=0),
        html.Button('График', id='chart_btn', n_clicks=0, style={'margin-left': '5px'})
    ], className='button_menu'),


    html.Div(id='container-button-timestamp'),

    html.Div([
        html.Div([
            dash_table.DataTable(
                id = 'funnel_villages',
                columns=[{"name": i, "id": i} for i in df_villages_default.columns],
                data=df_villages_default.to_dict('records'),
                editable=False,
                sort_action='native',
                style_table={'height': '75vh', 'overflowY': 'auto'}
            )]
    )],className='villages_table', id='villages_table'),



    html.Div([
        dcc.Graph(
            id='village_graph',
            figure=generate_bar_chart(list(df_villages.index),
                                      list(df_villages.values),
                                      'Распределение игроков на эпохах по датам'),
            style={'width': '800px', 'height': '400px', 'border': '1px solid lightgray'}

        )
    ], className='villages_chart', id='villages_chart')

    ], className='tabs_main_div')




@app.callback([Output('villages_table', 'style'),
               Output('villages_chart', 'style')],
              [Input('table_btn', 'n_clicks'),
               Input('chart_btn', 'n_clicks')])
def displayChart(btn1, btn2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'table_btn' in changed_id:
        return {'display': 'block'}, {'display': 'none'}
    elif 'chart_btn' in changed_id:
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'block'}, {'display': 'none'}


@app.callback(
    [Output('funnel_villages', 'data'),
     Output('funnel_villages', 'columns'),
     Output('village_graph', 'figure')],
    [Input('start_date_funnel_villages', 'date'),
     Input('end_date_funnel_villages', 'date')]
)
def update_data(start_date, end_date):

    df = df_buildings.loc[(df_buildings['Date'] >= pd.to_datetime(start_date)) & (df_buildings['Date'] <= pd.to_datetime(end_date))
                        & (df_buildings['name'] == 'village_unlocked')
                        ].drop(columns=['name', 'Building', 'Stage'])

    df_villages = df_buildings.loc[(df_buildings['Date'] >=  pd.to_datetime(start_date)) & (df_buildings['Date'] <= pd.to_datetime(end_date))
                     & (df_buildings['name'] == 'village_unlocked')].drop(columns=['name']).groupby('Village')['User_id'].nunique()

    chart_data = generate_bar_chart(list(df_villages.index), list(df_villages.values), 'Распределение игроков на эпохах по датам')

    data = df.to_dict('rows')
    columns = [{"name": i, "id": i} for i in df.columns]
    return data, columns, chart_data