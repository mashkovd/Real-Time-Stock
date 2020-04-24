# -*- coding: utf-8 -*-
import dash
# import dash_auth
from dash.dependencies import Input, Output

from dash_package.dbc_comp import *
from dash_package import r15

import pandas as pd
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_app = dash.Dash(__name__,
                     # requests_pathname_prefix='/stock/',
                     external_stylesheets=[dbc.themes.BOOTSTRAP],
                     # assets_external_path='http://your-external-assets-folder-url/',
                     meta_tags=[
                         {
                             'name': 'description',
                             'content': 'Real-time stocks'
                         },
                         {
                             'name': 'viewport',
                             'content': 'width=device-width'
                         }
                     ]
                     )

# VALID_USERNAME_PASSWORD_PAIRS = [('ftt', '12345')]
#
# auth = dash_auth.BasicAuth(
#     docker_dash_app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )
# with open('./template/index.html') as f:
#     docker_dash_app.index_string = f.read()

dash_app.title = "RTS"
dash_app.layout = html.Div(children=[
    # nav,
    body,
    timer,

])


@dash_app.callback(Output('stock_graph_day', 'figure'),
                   [
                       Input('interval-component-day', 'n_intervals'),
                       Input('stocks-dropdown', 'value'),
                       Input('interval-dropdown', 'value'),
                       Input('value-dropdown', 'value'),
                       Input('ascending-dropdown', 'on'),

                   ]
                   )
def update_graph_live(n, stocks, interval, value, ascending, ):
    # {'o': 11.0, 'c': 46.0, 'h': 28.0, 'l': 3.0, 'v': 951, 'time': '2020-02-01 15:11:10', 'interval': '1min',
    #  'figi': 'BBG000BBR9P6', 'name': '1-800-Flowers.com Inc'}
    stocks_count = 15
    stock_data = [json.loads(figi_data) for figi_data in
                  [r15.hget(item.decode("utf-8"), str(interval)) for item in r15.keys()] if figi_data is not None]
    if stocks is not None and stocks:
        stock_data = [item for item in stock_data if item.get('figi') in stocks]
        stocks_count = len(stocks)

    df = pd.DataFrame(stock_data)

    if not df.empty:
        df['delta'] = df.apply(lambda row: (row['c'] - row['o']) / row['o'] * 100 if row['o'] != 0 else 0, axis=1)
        df = df.sort_values(value, ascending=not bool(ascending)).copy()
        df = df.head(stocks_count)
    else:
        return {
            'data': [],
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No matching data found",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            }
        }

    figure = {
        'data': [
            {'x': df.name, 'y': df[value],
             'type': 'bar',
             'marker': {
                 'color': '#ABE2FB',
             },
             },
            # {'x': df.name, 'y': df['c'], 'type': 'bar'},
        ],
        'layout': {
            # 'title': 'График'
        }
    }

    return figure


# @docker_dash_app.callback(
#     Output("graph_day_col", "md"),
#     [Input("collapse-button", "n_clicks")],
# )
# def toggle_collapse(n):
#     return 12 if n is None else ((n + 1) % 2 + 1) * 6


# @docker_dash_app.callback(Output('stock_graph_volume', 'figure'),
#                    [
#                        Input('interval-component-day', 'n_intervals'),
#                        Input('stocks-dropdown', 'value'),
#                        Input('interval-dropdown', 'value'),
#                        Input('value-dropdown', 'value'),
#                        Input('ascending-dropdown', 'on'),
#                    ]
#                    )
# def update_graph_live(n, stocks, interval, value, ascending, ):
#     stocks_count = 20
#
#     if stocks is not None and stocks:
#         stocks_count = len(stocks)
#     else:
#         return {}
#
#     df = get_historical_data(stocks[0], interval=interval)
#
#     # df['color'] = df.apply(lambda row: 'red' if (row['c'] - row['o']) < 0 else 'green', axis=1)
#     df = df.sort_values('time').copy()
#     df['color'] = df.apply(lambda row: 'red' if (row['c'] - row['o']) < 0 else 'green', axis=1)
#     # df = df.sort_values('time').copy()
#     figure = {
#         'data': [
#             {
#                 'x': df.time,
#                 'open': df.o,
#                 'close': df.c,
#                 'high': df.h,
#                 'low': df.l,
#                 'volume': df.v,
#                 'type': 'candlestick',
#
#             },
#             {
#                 'x': df.time,
#                 'y': df.v/100,
#                 # 'close': df.c,
#                 # 'high': df.h,
#                 # 'low': df.l,
#                 # 'volume': df.v,
#                 'type': 'bar',
#
#             },
#         ],
#         'layout': {
#             # 'title': 'График'
#         }
#     }
#     return figure


@dash_app.callback(Output('interval-component-day', 'interval'),
                   [
                       Input('reload-switch', 'on'),

                   ]
                   )
def update_graph_live(value):
    if value:
        return 5 * 1000
    else:
        return 60 * 60 * 1000


if __name__ == '__main__':
    dash_app.run_server(debug=True, port=5000, host="0.0.0.0")
