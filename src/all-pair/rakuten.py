import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../packages'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../spreads_handler'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))
import time
from handlers.rakuten_spreds_handler import RakutenSpreadsHandler
from config import Config
from anouncer import Anouncer

cfg = Config("./config.json")
anouncer = Anouncer()
current_spread_list = []
handler = RakutenSpreadsHandler(cfg.pair)
#lastbid = None
while True:
    try:
        spred_list = handler.get_spread_list()
        for spread_dict in spred_list:
            pair_name = spread_dict['pair_name']
            spread = spread_dict['spread']
            if len(current_spread_list) > 0 and pair_name:
                current_spread_dict = next(filter(lambda x: x['pair_name'] == pair_name, current_spread_list), None)
                if current_spread_dict and spread and current_spread_dict['spread'] != spread: 
                    print("old_value" + str(current_spread_dict) + ", new-value: " + str(spread_dict))
                    anouncer.anounce_msg(str(current_spread_dict['pair_name']) + handler.get_spread_for_anounce_from(spread))
        current_spread_list = spred_list
    except Exception as e:
        print(e)
        err_msg = "エラーが発生しました。処理を終了します。"
        print(err_msg)
        anouncer.anounce_msg(err_msg)
        handler.quit_driver()
        break
    finally:
        print("--------------------------")
    time.sleep(cfg.time_interval)
 