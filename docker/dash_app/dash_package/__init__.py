from redis import Redis
import os
import json

r15 = Redis(host=os.getenv('redis_host'), port=6379, db=15, password=None)

stock_data = [json.loads(figi) for figi in [r15.hget(item.decode("utf-8"), '6') for item in r15.keys()]]
figi = [dict(label=item.get('name'), value=item.get('figi')) for item in stock_data]
