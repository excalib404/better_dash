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

########### tab 4 - buildings

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

df_buildings_default = df_buildings.loc[
    (df_buildings['Date'] >= start_date_default) & (df_buildings['Date'] <= end_date_default)
    & (df_buildings['name'] == 'village_building_updated')].drop(columns=['name'])

# Построенно/Пофикшенное количество зданий
buildings_updated = len(
    df_buildings.loc[(df_buildings['Date'] >= start_date_default) & (df_buildings['Date'] <= end_date_default)
                     & (df_buildings['name'] == 'village_building_updated')
                     & (df_buildings['Village'] != 1)
                     & (df_buildings['Building'] != 'TypeA')].drop(columns=['name']))
buildings_fixed = len(
    df_buildings.loc[(df_buildings['Date'] >= start_date_default) & (df_buildings['Date'] <= end_date_default)
                     & (df_buildings['name'] == 'village_building_fixed')].drop(columns=['name']))

# Для графиков
buildings_chart_labels = ['Построено зданий', 'Починено зданий']
bar_color = ['#304860' for n in range(1, 13)]


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
            dcc.DatePickerSingle(id='start_date_funnel_buildings', style={'float': 'left', 'height': '36px'},
                                 date=datetime(date_default.year, date_default.month, 1),
                                 placeholder='Start date',
                                 display_format='D MMMM YYYY'),

            html.Div([html.H5('-')], style={'float': 'left', 'margin-left': '5px', 'margin-right': '5px'}),
            dcc.DatePickerSingle(id='end_date_funnel_buildings', className='end_date',
                                 date=datetime(date_default.year, date_default.month, date_default.day),
                                 placeholder='End date',
                                 display_format='D MMMM YYYY')

        ], className='date_select_wrapper fm_element'),

        html.Div([
            html.Label('Выбор действия', className='label'),
            dcc.Dropdown(
                id='building_actions_dropdown', className='building_actions_dropdown',
                options=[
                    {'label': 'Улучшение постройки', 'value': 'building_upgrade'},
                    {'label': 'Починка постройки', 'value': 'building_repair'},
                    {'label': 'График построек/починок', 'value': 'building_chart'}
                ], style={'color': 'black', 'height': '38px'},
                searchable=False, clearable=False,
                value='building_upgrade'
            )
        ], className='dropdown_wrapper fm_element'),

        html.Div([
            html.Label('Выбор типа', className='label'),
            dcc.Dropdown(id='data_type_dropdown')
        ], className='dropdown_wrapper fm_element', id='data_type_wrapper', style={'display': 'none'}),
        # html.Div([html.Button('Подтвердить', id='submit_btn', n_clicks=0)], className='btn_wrapper fm_element'),
    ], className='filter_menu'),

    html.Div([
        html.Div([
            dash_table.DataTable(
                id='funnel_buildings',
                columns=[{"name": i, "id": i} for i in df_buildings_default.columns],
                data=df_buildings_default.to_dict('records'),
                editable=False,
                sort_action='native',
                style_table={'height': '75vh', 'overflowY': 'auto'}
            )]
        )], className='buildings_table', id='buildings_table'),

    html.Div([
        dcc.Graph(
            id='buildings_graph',
            figure=generate_bar_chart(buildings_chart_labels,
                                      [buildings_updated, buildings_fixed],
                                      'График построек и починок зданий'),
            style={'width': '800px', 'height': '400px', 'border': '1px solid lightgray'}
        )
    ], className='buildings_chart', id='buildings_chart')

], className='tabs_main_div')



# Tab 4 callback
@app.callback(
    [Output('funnel_buildings', 'data'),
     Output('funnel_buildings', 'columns'),
     Output('buildings_graph', 'figure'),
     Output('buildings_table', 'style'),
     Output('buildings_chart', 'style')],
    [Input('start_date_funnel_buildings', 'date'),
     Input('end_date_funnel_buildings', 'date'),
     Input('building_actions_dropdown', 'value')]
)
def page_4_update_table(start_date, end_date, building_action):

    bar_chart = generate_bar_chart(buildings_chart_labels, [buildings_updated, buildings_fixed], 'График построек и починок зданий')
    buildings_table_style = {}
    buildings_chart_style = {}
    if building_action == 'building_upgrade':
            df = df_buildings.loc[(df_buildings['Date'] >= pd.to_datetime(start_date)) & (df_buildings['Date'] <= pd.to_datetime(end_date))
                        & (df_buildings['name'] == 'village_building_updated')
                        ].drop(columns=['name'])
            buildings_table_style = {'display': 'block'}
            buildings_chart_style = {'display': 'none'}
    elif building_action == 'building_repair':
            df = df_buildings.loc[(df_buildings['Date'] >= pd.to_datetime(start_date)) & (df_buildings['Date'] <= pd.to_datetime(end_date))
                        & (df_buildings['name'] == 'village_building_fixed')
                        ].drop(columns=['name'])
            buildings_table_style = {'display': 'block'}
            buildings_chart_style = {'display': 'none'}
    elif building_action == 'building_chart':
            df = df_buildings.loc[(df_buildings['Date'] >= pd.to_datetime(start_date)) & (df_buildings['Date'] <= pd.to_datetime(end_date))
                        & (df_buildings['name'] == 'village_unlocked')
                        ].drop(columns=['name', 'Building', 'Stage'])
            buildings_updated_new = len(df_buildings.loc[(df_buildings['Date'] >= pd.to_datetime(start_date))
                                                         & (df_buildings['Date'] <= pd.to_datetime(end_date))
                                                         & (df_buildings['name'] == 'village_building_updated')
                                                         & (df_buildings['Village'] != 1)
                                                         & (df_buildings['Building'] != 'TypeA')].drop(columns=['name']))

            buildings_fixed_new = len(df_buildings.loc[(df_buildings['Date'] >= pd.to_datetime(start_date))
                                                       & (df_buildings['Date'] <= pd.to_datetime(end_date))
                                                       & (df_buildings['name'] == 'village_building_fixed')].drop(columns=['name']))
            bar_chart = generate_bar_chart(buildings_chart_labels,
                                           [buildings_updated_new, buildings_fixed_new],
                                           'График построек и починок зданий')
            buildings_table_style = {'display': 'none'}
            buildings_chart_style = {'display': 'block'}

    data = df.to_dict('rows')
    columns = [{"name": i, "id": i} for i in df.columns]
    return data, columns, bar_chart, buildings_table_style, buildings_chart_style

