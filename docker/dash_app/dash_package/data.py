interval_marks = {
    6: '1м',
    7: '2м',
    # 9: '3м',
    # 5: '15м',
    10: '5м',
    # 4: '10м',
    # 8: '30м',
    # 1: 'час',
    0: 'день',
}

asc_options = [
    {'label': 'Падение', 'value': False},
    # {'label': 'Падение', 'value': False},
]

value_options = [
    {'label': 'Изменение, %', 'value': 'delta'},
    {'label': 'Объем, ед.', 'value': 'v'},
    # {'label': 'Объем * стоимость', 'value': 'c'},
]

time_options = [
    {'label': '2 сек', 'value': 2 * 1000},
    {'label': '5 сек', 'value': 5 * 1000},
    {'label': '10 сек', 'value': 10 * 1000},
]

intervals = ['day', 'hour', 'month', 'week', '10min', '15min', '1min', '2min', '30min', '3min', '5min']
