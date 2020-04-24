from openapi_client.openapi_streaming import run_stream_consumer, print_event, do_nothing
from openapi_client.openapi import sandbox_api_client
from openapi_genclient.models.candle_resolution import CandleResolution
import multiprocessing as mp
import fire
import json
import time
from redis import Redis
import os

r15 = Redis(host=os.getenv('redis_host'), port=6379, db=15, password=None)
r14 = Redis(host=os.getenv('redis_host'), port=6379, db=14, password=None)
token = os.getenv('tinkoff_token')

# для получения списка бумаг необходимо указать токен для торговли
# client = sandbox_api_client(token)
# stocks = client.market.market_stocks_get()
# stocks_dct = {item.figi: {'name': item.name} for item in stocks.payload.instruments}
with open('stocks.json', 'r') as fp:
    stocks_dct = json.load(fp)

intervals = list({key: getattr(CandleResolution, key) for key in (dir(CandleResolution))[:11]}.values())
print(f'Count of stocks is {len(stocks_dct)}')


def to_redis(event):
    figi = event.get('figi')
    interval = intervals.index(event.get('interval'))
    event.update(**stocks_dct.get(figi))
    b_event = json.dumps(event)

    t = time.strptime(event.get('time'), "%Y-%m-%dT%H:%M:%SZ")
    if interval == 6:
        hour = t.tm_hour
        minute = t.tm_min
        r14.hset(figi, f'{interval + minute * 100 + hour * 10000}', b_event)
    r15.hset(figi, interval, b_event)


func = dict(do_nothing=do_nothing, to_redis=to_redis, print_event=print_event)


def get_stock_data(interval_='day',
                   depth_=5,
                   i=0,
                   **kwargs
                   ):
    """ Получаем данные по подписке

    Args:
        i:
        interval_: Интервал свечи
        depth_: Глубина стакана [1..20]
        **kwargs: словарь содержит информацию о подписках и

    Returns:
        None

    """

    subs_dct = [dict(figi=item, interval=interval_, depth=depth_) for item in list(stocks_dct)]
    candle_subs = kwargs.get('candle_subs', subs_dct)
    orderbook_subs = kwargs.get('orderbook_subs', subs_dct)
    instrument_info_subs = kwargs.get('instrument_info_subs', subs_dct)

    print(f'{mp.current_process().name} is on')
    while True:
        try:
            run_stream_consumer(token,
                                candle_subs,
                                orderbook_subs,
                                instrument_info_subs,
                                on_candle_event=kwargs.get('on_candle_event', do_nothing),
                                on_orderbook_event=kwargs.get('on_orderbook_event', do_nothing),
                                on_instrument_info_event=kwargs.get('on_instrument_info_event', do_nothing)
                                )
        except Exception as err:
            print(f'{mp.current_process().name} restart{err}')
            time.sleep(30)
            print('restart start ')

    # while True:
    #     price = random.randint(-250, 250)
    #     event = {'o': price + random.randint(-20, 20),
    #              'c': price + random.randint(-20, 20),
    #              'h': price + random.randint(-30, 30),
    #              'l': price + random.randint(-25, 25),
    #              'v': random.randint(0, 1000),
    #              'time': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
    #              'interval': interval_,
    #              'figi': list(stocks_dct)[random.randint(0, 1000)]}
    #     to_redis(event)
    #     time.sleep(1)


def run_process(intervals_,
                **kwargs):
    for key, value in kwargs.items():
        kwargs.update({key: func.get(value, value)})
    l_process = []
    for i, interval in enumerate(intervals_):
        process = mp.Process(target=get_stock_data,
                             args=(interval, 5, i),
                             kwargs=kwargs,
                             name=f'Interval - {interval}',
                             daemon=True
                             )
        process.start()

        l_process.append(process)
    for process in l_process:
        process.join()
    print(f'{mp.current_process().name} is off')


if __name__ == '__main__':
    print(f'subscribe to stock {time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}')
    fire.Fire(run_process, [
        # '-candle_subs=()'
        '-orderbook_subs=()',
        '-instrument_info_subs=()',
        '-on_candle_event=to_redis',
        '-on_orderbook_event=do_nothing',
        '-on_instrument_info_event=do_nothing',
        '['
        # ' "day",'
        # ' "hour",'
        # ' "month",'
        # ' "week",'
        # ' "10min",'
        # ' "15min",'
        ' "1min",'
        # ' "2min",'
        # ' "30min",'
        # ' "3min",'
        # ' "5min"'
        ']'
    ])

# [(0, 'day'),
#  (1, 'hour'), -
#  (2, 'month'),
#  (3, 'week'),
#  (4, '10min'),-
#  (5, '15min'),
#  (6, '1min'),-
#  (7, '2min'),-
#  (8, '30min'),
#  (9, '3min'),
#  (10, '5min')]-
