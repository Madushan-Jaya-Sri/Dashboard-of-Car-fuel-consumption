import dash
# import dash_core_components as dcc
import dash_bootstrap_components as dbc
# import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash import Input, Output, html
from dash import dcc

car_fuel = pd.read_excel('car_fuel.xlsx')
car_fuel["Gas re fill season"] = car_fuel["gas_type"] + "_" + car_fuel["gas_type_code"].astype(str)
car_fuel[['specials']] = car_fuel[['specials']].fillna('no special')
tem_inside_mean = car_fuel['temp_inside'].mean()
car_fuel[['temp_inside']] = car_fuel[['temp_inside']].fillna(tem_inside_mean)
hdf = px.data.medals_wide(indexed=True)

correlation = car_fuel.corr()

# Create a DataFrame object from list
data_set = pd.DataFrame(correlation, columns=["distance", "Consumption", "speed", "temp_inside", "temp_outside"])
data_heat_map = data_set.loc[["distance", "Consumption", "speed", "temp_inside", "temp_outside"]]

Corre = pd.DataFrame(data_heat_map)

car_fuel_AC = car_fuel[['gas_type', 'AC', 'Consumption']].groupby(['gas_type', 'AC']).mean('Consumption').reset_index()
car_fuel_rain = car_fuel[['gas_type', 'rain', 'Consumption']].groupby(['gas_type', 'rain']).mean(
    'Consumption').reset_index()
car_fuel_sun = car_fuel[['gas_type', 'sun', 'Consumption']].groupby(['gas_type', 'sun']).mean(
    'Consumption').reset_index()
car_fuel_AC = car_fuel_AC[car_fuel_AC['AC'] == 1].reset_index()
car_fuel_rain = car_fuel_rain[car_fuel_rain['rain'] == 1].reset_index()
car_fuel_sun = car_fuel_sun[car_fuel_sun['sun'] == 1].reset_index()

car_fuel_AC['new'] = ['AC', 'AC']
car_fuel_rain['new'] = ['rain', 'rain']
car_fuel_sun['new'] = ['sun', 'sun']
data_bar = pd.concat([car_fuel_AC, car_fuel_rain, car_fuel_sun]).rename(
    columns={'Consumption': 'AVG_Consumption', 'new': 'Special_condition'})
fig22 = px.bar(data_bar, x='Special_condition', y='AVG_Consumption', color='gas_type', barmode='group')

pie_chart = px.pie(car_fuel, 'gas_type', hole=.4)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

app.layout = dbc.Container(
    [dbc.Row([
        dbc.Col(
            html.Div(
                style={
                    # 'background-image': "url(https://cutewallpaper.org/21/black-abstract-background/Black-Abstract-Wallpapers-Top-Free-Black-Abstract-.jpg)",

                    # 'background': "linear-gradient(#45171d, #e84a5f)",
                    'background-color': '#000000',
                    'background-repeat': ' no-repeat',
                    'background-attachment': 'fixed',
                    'background-size': 'cover',
                },
                children=[
                    dbc.Row([
                        dbc.Col(
                            html.Div(children=[
                                html.P("----------Dashboard of Car-fuel consumption----------",
                                       className="text-white text-center font-weight-bolder",
                                       style={'font-size': '30px', 'background-color': '#034f84'})

                            ]), width={'size': 12}

                        )
                    ], justify='center'),
                    dbc.Row([
                        dbc.Col(
                            html.Div(
                                children=[
                                    dbc.Row([
                                        dbc.Col(
                                            html.Div(
                                                children=[
                                                    dbc.RadioItems(
                                                        id="radio",
                                                        options=[{"label": "Consumption", "value": 'Consumption'},
                                                                 {"label": "Cost", "value": 'Cost'},
                                                                 ],
                                                        label_style={'color': '#ff8364', 'font-weight': 'bold',
                                                                     'font-size': '20px'},
                                                        value='Consumption', inline=True,
                                                    ),
                                                    dcc.Graph(id='Boxplot',
                                                              style={'height': '450px', 'width': '100%'})
                                                ]
                                            ), className="p-2"
                                        )
                                    ], className="h-75 p-1"),
                                    dbc.Row([
                                        dbc.Col(
                                            html.Div(
                                                children=[
                                                    dbc.Carousel(

                                                        items=[
                                                            {"key": "1", "src": "/static/images/E1.png.jpg"},
                                                            {"key": "2", "src": "/static/images/E2.png.jpg"},
                                                            {"key": "3", "src": "/static/images/E3.png.jpg"},
                                                            {"key": "4", "src": "/static/images/E4.png.jpg"},
                                                            {"key": "5", "src": "/static/images/E5.png.jpg"},
                                                            {"key": "6", "src": "/static/images/SP98_1.png.jpg"},
                                                            {"key": "7", "src": "/static/images/SP98_2.png.jpg"},
                                                            {"key": "8", "src": "/static/images/SP98_3.png.jpg"},
                                                            {"key": "9", "src": "/static/images/SP98_4.png.jpg"},
                                                            {"key": "10", "src": "/static/images/SP98_5.png.jpg"},
                                                            {"key": "11", "src": "/static/images/SP98_6.png.jpg"},

                                                        ],
                                                        controls=True,
                                                        indicators=True,
                                                        interval=1500,
                                                        ride="carousel",

                                                    )

                                                ],
                                            ), width=6
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                children=[
                                                    html.P("Trips",
                                                           className="text-white text-center font-weight-bolder",
                                                           style={'font-size': '20px', 'font-type': 'italic',
                                                                  'background-color': '#034f84'}),
                                                    dcc.Graph(id="pie-chart",
                                                              figure=pie_chart,
                                                              style={'height': '220px', 'width': '100%'}
                                                              ),

                                                ]
                                            ), width=6, className="p-1"
                                        )
                                    ], className="h-25")
                                ]
                            ),
                            width={'size': 4}
                        ),
                        dbc.Col(
                            html.Div(
                                children=[
                                    dbc.Row([
                                        dbc.Col(
                                            html.Div(children=[

                                                dcc.Dropdown(

                                                    id='fuel-dropdown',
                                                    clearable=False,
                                                    style={

                                                        # 'display': 'inline-block',
                                                        'width': '100%',
                                                        'background-color': '#ff8364',

                                                        'color': 'Black', 'font-size': '20px',

                                                    },

                                                    options=[{'label': i, 'value': i}
                                                             for i in
                                                             (car_fuel['Gas re fill season'].unique())],
                                                    value='E10_1',
                                                ),

                                                dcc.Graph(id='distance-graph',
                                                          style={'height': '350px', 'width': '100%'})
                                            ])
                                            , width={'size': 8}
                                        ),
                                        dbc.Col(
                                            children=[

                                                dcc.Checklist(
                                                    id='medals',
                                                    options=[{'label': x, 'value': x}
                                                             for x in Corre.columns],
                                                    value=Corre.columns.tolist(),
                                                ),
                                                dcc.Graph(id="graph",
                                                          style={'height': '320px', 'width': '99%'}),

                                            ],
                                            width={'size': 4, 'offset': 0},
                                            className="p-2"
                                        )
                                    ], className="p-1"),
                                    dbc.Row([
                                        dbc.Col(
                                            html.Div(
                                                children=[

                                                    dcc.Graph(id="Bar-chart",

                                                              figure=fig22,
                                                              style={'height': '375px', 'width': '100%',
                                                                     'plot_bgcolor': '#04180D',
                                                                     'paper_bgcolor': '#04042E',
                                                                     'font_color': '#7FDBFF'},

                                                              )

                                                ],
                                            ),
                                            width={'size': 6}
                                        ),
                                        dbc.Col(
                                            children=[
                                                dcc.Dropdown(

                                                    options=[{'label': 'Consumption', 'value': 'Consumption'},
                                                             {'label': 'speed', 'value': 'speed'},
                                                             {'label': 'distance', 'value': 'distance'}],
                                                    optionHeight=20,
                                                    style={'width': '100%', 'background-color': '#ff8364',
                                                           'color': 'Black', 'font-size': '20px'},
                                                    placeholder='Choose X',
                                                    clearable=False,
                                                    id="dpm_xaxis",
                                                    value='Consumption'

                                                ),

                                                dcc.Graph(id='Scatter-plot',

                                                          style={'height': '300px', 'width': '100%'},

                                                          ),
                                                dcc.Dropdown(

                                                    options=[{'label': 'Consumption', 'value': 'Consumption'},
                                                             {'label': 'speed', 'value': 'speed'},
                                                             {'label': 'distance', 'value': 'distance'}],
                                                    optionHeight=20,
                                                    style={'width': '100%', 'background-color': '#ff8364',
                                                           'color': 'Black', 'font-size': '20px'},
                                                    placeholder='Choose Y',
                                                    clearable=False,

                                                    id="dpm_yaxis",
                                                    value='distance'

                                                ),

                                            ],
                                            width={'size': 6}, className="p-1"
                                        )
                                    ],
                                        className="p-1")
                                ]
                            ), width={'size': 8}, className="p-0"
                        )
                    ], justify='center', className="p-1")
                ]
            ), width={'size': 12})
    ], )
    ], fluid=True)


@app.callback(
    Output(component_id='Boxplot', component_property='figure'),
    Input(component_id='radio', component_property='value'), )
def update_boxplot(y_axis):
    dff = car_fuel
    fig = px.box(dff, x=car_fuel.gas_type, y=y_axis)
    fig.update_traces(boxmean='sd')
    fig.update_layout(margin=dict(l=0, r=30, t=50, b=50),
                      title=y_axis + ' Vs Fuel Type',
                      title_font_size=20,
                      title_pad=dict(l=90, r=0, t=0, b=0),
                      yaxis=dict(
                          autorange=True,
                          showgrid=True,
                          zeroline=True, zerolinewidth=2,
                          gridcolor='#7FDBFF', gridwidth=1,
                          title_font_size=15),
                      xaxis=dict(
                          title_text='Fuel Type',
                          title_font_size=15),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      font_color='#7FDBFF'
                      )
    return fig


@app.callback(
    Output(component_id='distance-graph', component_property='figure'),
    Input(component_id='fuel-dropdown', component_property='value')
)
def update_graph(selected_gas):
    filtered_fuel = car_fuel[car_fuel['Gas re fill season'] == selected_gas]
    line_fig = px.line(filtered_fuel, y='distance')

    line_fig.update_xaxes(title_text='trip')
    line_fig.update_yaxes(title_text='Distance')
    line_fig.update_layout(

        margin=dict(l=0, r=10, t=30, b=0),

        title_font_size=25,

        title_pad=dict(l=100, r=0, t=0, b=0),

        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,

            gridcolor='#7FDBFF',
            gridwidth=1,

            zerolinewidth=2,

            title_font_size=20),
        xaxis=dict(

            title_font_size=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#7FDBFF'

    )

    return line_fig


@app.callback(
    Output(component_id="graph", component_property="figure"),
    [Input(component_id="medals", component_property="value")])
def filter_heatmap(cols):
    fig = px.imshow(Corre[cols])
    fig.update_layout(

        margin=dict(l=0, r=10, t=30, b=0),
        title_font_size=25,

        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,

            gridcolor='#7FDBFF',
            gridwidth=1,

            zerolinewidth=2,

            title_font_size=20),
        xaxis=dict(

            title_font_size=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#7FDBFF'

    )
    return fig


@app.callback(
    Output(component_id='Scatter-plot', component_property='figure'),
    Input(component_id='dpm_yaxis', component_property='value'),
    Input(component_id='dpm_xaxis', component_property='value'))
def update_scatterplot(xaxis, yaxis):
    dff = car_fuel
    scatter = px.scatter(dff, x=xaxis, y=yaxis, )

    scatter.update_layout(

        margin=dict(l=0, r=10, t=50, b=0),
        title=yaxis + ' Vs ' + xaxis,
        title_font_size=20,

        title_pad=dict(l=150, r=0, t=50, b=0),

        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,

            gridcolor='#7FDBFF',
            gridwidth=1,

            zerolinewidth=2,

            title_font_size=20),
        xaxis=dict(

            title_font_size=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#7FDBFF'

    )

    return scatter


fig22.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#7FDBFF',
                    title="Avg. consumption under special conditions",
                    title_font_size=20,
                    title_font_family='Raleway',
                    title_pad=dict(l=80, r=0, t=50, b=0),
                    margin=dict(l=20, r=10, t=100, b=0),

                    )
pie_chart.update_layout(

    margin=dict(l=10, r=0, t=10, b=10),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',

    font_color='#7FDBFF'

)

if __name__ == '__main__':
    app.run_server(debug=True)
