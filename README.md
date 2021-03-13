Telegram Bot for cryptocurrency monitoring.
Main pairs:
['BTC_ETH', 'ETH_BTC', 'BTC_USDT', 'ETH_UAH', 'USDT_UAH', 'ETH_USDT', 'BTC_UAH']

**in docker-compose.yml:**
    _environment:
      - TOKEN=***_
replace *** for your BOT TOKEN (without quotes!!!)

**tbot/celery.py**
line 18:
        _'schedule': 1.0,_
if you want - you can change update interval - default 1 second.

**$ sudo docker-compose build 
$ sudo docker-compose up**

then - push /start 



