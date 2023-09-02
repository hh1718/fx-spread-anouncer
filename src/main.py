import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'packages'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'spreads_handler'))
import json
import time
import pyttsx3

from config import Config
from anouncer import Anouncer
from handlers.gaikaex_spreds_handler import GaikaexSpreadsHandler
from handlers.gaitame_spreds_handler import GaitameSpreadsHandler
from handlers.rakuten_spreds_handler import RakutenSpreadsHandler


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    cfg = Config(parent_dir + "/config.json")
    pair = cfg.pair
    logging = cfg.logging
    force_anounce_per = cfg.force_anounce_per
    anounce_order = cfg.anounce_order
    if len(anounce_order) <= 0:
        print()
        print("anounce_order is not defined.")
        print()
        return
    handlers = []
    for key in anounce_order:
        if key == "gaikaex":
            handlers.append({ "key": key, "handler": GaikaexSpreadsHandler(pair, logging) })
        elif key == "gaitame":
            handlers.append({ "key": key, "handler": GaitameSpreadsHandler(pair, logging) })
        elif key == "rakuten":
            handlers.append({ "key": key, "handler": RakutenSpreadsHandler(pair, logging) })
    anouncer = Anouncer()
    i = 1
    while True:
        try:
            is_spread_changed = False
            for handler in handlers:
                h = handler.get("handler")
                h.update_spread()
                if h.is_spread_changed():
                    is_spread_changed = True
            
            if is_spread_changed or (i >= force_anounce_per and force_anounce_per != 0):
                anounce_msg = ""
                for handler in handlers:
                    anounce_msg = anounce_msg + handler.get("handler").get_spread_for_anounce() + "。"
                if anounce_msg != "":
                    anouncer.announce_spread(anounce_msg)
        except Exception as e:
            print(e)
            err_msg = "エラーが発生しました。処理を終了します。"
            print(err_msg)
            anouncer.anounce_msg(err_msg)
            for handler in handlers:
                handler.get("handler").quit_driver()
            break
        finally:
            if i >= force_anounce_per:
                i = 1
            else:
                i = i + 1
            if logging:
                print("--------------------------")
        time.sleep(cfg.time_interval)

main()
 