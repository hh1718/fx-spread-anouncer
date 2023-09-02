import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../packages'))
import requests
import pyttsx3
import time
from decimal import Decimal, ROUND_HALF_UP

engine = pyttsx3.init()
current_spread_list = []
idx = 0
while idx <= 1000:
    url = "https://navi.gaitame.com/v3/info/prices/rate"
    res = requests.get(url, params={})
    res_json = res.json()
    if res_json['status'] != 200:
        print("error: " + str(res_json['status']))
        continue
    new_spread_list = []
    for rate in res_json['data']:
        pair = rate['pair']
        ask_value = rate['ask']
        bid_value = rate['bid']
        spread = None
        if bid_value and ask_value:
            ask = Decimal(rate['ask'])
            bid = Decimal(rate['bid'])
            spread = (ask - bid).quantize(Decimal('0.0000001'), rounding=ROUND_HALF_UP)
        spread_dict = {'pair': pair, 'spread': spread, 'bid': bid_value, 'ask': ask_value }
        #print(spread_dict)
        new_spread_list.append(spread_dict)
        if len(current_spread_list) > 0:
            current_spread_dict = next(filter(lambda x: x['pair'] == pair, current_spread_list), None)
            if current_spread_dict and spread: 
                if current_spread_dict['spread'] != spread:
                    print("old_value" + str(current_spread_dict) + ", new-value: " + str(spread_dict))
                    engine.say(pair + "のスプレッドは" + str(spread) + "です")
                    engine.runAndWait()

    current_spread_list = new_spread_list
    print("--------------------------")
    idx = idx + 1
    time.sleep(3)
 


