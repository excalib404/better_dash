import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from tabs import tab1, tab2, tab3, tab4, tab5, tab6, tab7

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab_1', vertical=True,
        children=[
        dcc.Tab(label='Main', value='tab_1'),
        dcc.Tab(label='Retention', value='tab_2'),
        dcc.Tab(label='Monetization', value='tab_3'),
        dcc.Tab(label='Tutorial', value='tab_4'),
        dcc.Tab(label='Spins', value='tab_5'),
        dcc.Tab(label='Buildings', value='tab_6'),
        dcc.Tab(label='Villages', value='tab_7')
        ], className='tab_menu'
    ),
    html.Div([html.Div(id='tabs_content')], className='content')
    ], className='main_wrapper')

@app.callback(Output('tabs_content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab_1':
        return tab1.layout
    if tab == 'tab_2':
        return tab2.layout
    if tab == 'tab_3':
        return tab3.layout
    if tab == 'tab_4':
        return tab4.layout
    if tab == 'tab_5':
        return tab5.layout
    if tab == 'tab_6':
        return tab6.layout
    if tab == 'tab_7':
        return tab7.layout


if __name__ == '__main__':
    app.run_server(debug=True)