import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash_package.data import interval_marks, value_options

from . import figi

nav = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Поддержать проект", href="https://paypal.me/mashkovd?locale.x=ru_RU")),
    ],
    brand="RTS",
    brand_href="#",
    sticky="top",
    fluid=True,

)

graph = html.Div([dcc.Graph(
    id='stock_graph_day',
    className='dark-theme-control'
    # className="mt-3",
)])

graph_volume = html.Div(dcc.Graph(
    id='stock_graph_volume',
    className='dark-theme-control'
    # className="mt-3",
),
    id='div_stock_graph_volume')

stocks = dcc.Dropdown(
    id='stocks-dropdown',
    options=figi,
    multi=True,
    placeholder='Выберите инструменты',
    className='dark-theme-control'
    # style={'width': '400px',
    #        'fontSize': '15px',
    #        'margin': '5px',
    #        'display': 'inline-block'},
)
interval = dcc.Slider(
    id='interval-dropdown',
    min=0,
    max=10,
    step=None,
    marks=interval_marks,
    value=6,
    included=False,
    className='dark-theme-control'
)
indicator = dbc.Select(
    id='value-dropdown',
    options=value_options,
    value='delta',
    className='dark-theme-control'
)
asc = daq.BooleanSwitch(
    id='ascending-dropdown',
    label='Падение/Рост',
    labelPosition='bottom',
    on=True,
    className='dark-theme-control'
    # style={'padding': '20px'}

)

reload = daq.BooleanSwitch(
    id='reload-switch',
    label='online',
    labelPosition='bottom',
    on=True,
    className='dark-theme-control'
    # style={'padding': '20px'}

)

# collapse = html.Div(
#     [
#         dbc.Button(
#             "Объемы",
#             id="collapse-button",
#             color="primary",
#             # style={'position': 'absolute !important',
#             #        'z-index': '10 !important',
#             #        'left': '0px !important',
#             #        'bottom': '20% !important',
#             #        'transform': 'rotate(270deg)',
#             #        '-ms-transform': 'rotate(270deg)',
#             #        '-moz-transform': 'rotate(270deg)',
#             #        '-webkit-transform': 'rotate(270deg)',
#             #        '-o-transform': 'rotate(270deg)'
#             #        }
#
#         ),
#
#     ],
#     className='btn-group-vertical'
#
# )

# update_timer = dcc.RadioItems(
#     id='update-dropdown',
#     options=time_options,
#     value=2 * 1000,
#     labelStyle={'display': 'inline-block'}
# )

timer = dcc.Interval(
    id='interval-component-day',
    interval=2 * 1000,  # in milliseconds
    n_intervals=1
)

body = dbc.Container(
    [

        dbc.Row([
            dbc.Col([stocks],
                    md=6,
                    sm=10,  # align, children, className, id, key, lg, loading_state, md, sm, style, width, xl, xs
                    ),
            dbc.Col([indicator, ], md=6, className='mb-3'),
        ],
            className="my-2 mx-2"
        ),

        dbc.Row(children=
        [

            dbc.Col([asc, ], md=6),
            dbc.Col([reload, ], md=6),

        ], ),

        dbc.Row(children=
        [

            dbc.Col([interval, ], md=12),

        ], ),

        dbc.Row(children=
        [

            dbc.Col([graph, ],
                    md=12,
                    id='graph_day_col',
                    ),
            # dbc.Col([graph_volume, ],
            #         md=12,
            #         id='graph_volume_col',
            #         ),

        ], ),

        # dbc.Row(children=
        # [
        #
        #     dbc.Col([collapse, ], width={'offset': 11}),
        #
        # ], ),

    ], fluid=True)
