import os, sys
#sys.path.append(os.path.join(os.path.dirname(__file__), '../packages'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../spreads_handler'))
import pyttsx3
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from decimal import Decimal, ROUND_HALF_UP

from spreads_handler import SpreadsHandler

class RakutenSpreadsHandler(SpreadsHandler):
    def __init__(self, pair, logging):
        super().__init__(pair, logging)

    def get_pair_name_from_pair(self, pair):
        pair_name_dict = {
            "usdjpy": "ドル/円",
            "eurjpy": "ユーロ/円",
            "gbpjpy": "ポンド/円",
            "audjpy": "豪ドル/円",
            "nzdjpy": "NZドル/円",
        }
        pair_name = pair_name_dict[pair]
        
        return pair_name

    def _generate_driver(self):
        print("generate rakuten driver")
        #if self.driver:
        #    print("driver is already exist!")
        #    return
        #url = "https://www.rakuten-sec.co.jp/smartphone/fx/charm/commission.html"
        url = "https://www.rakuten-sec.co.jp/web/market/fisco/list.html"
        r = requests.get(url, params={})
        if r.status_code != 200:
            print("error: " + str(r.status_code))
            return
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        #options.headless = True
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.get(url)

        return self.driver

    #"https://www.rakuten-sec.co.jp/smartphone/fx/charm/commission.html"
    def update_spread_old(self):
        spread = None

        target_pair_name = self.get_pair_name_from_pair(self.pair)
        table_div = self.driver.find_element(By.ID, "rate-list-area")
        table = table_div.find_element(By.TAG_NAME, 'table')
        table_html = table.get_attribute('outerHTML')
        soup_table = BeautifulSoup(table_html, features="html.parser")
        tbody = soup_table.find('tbody')
        tr_list = tbody.find_all('tr')

        for tr in tr_list:
            td_list =  tr.find_all('td')
            pair_name_dom = td_list[0]
            pair_name = None
            if pair_name_dom:
                pair_name = pair_name_dom.text

            if target_pair_name == pair_name:
                spread_dom = td_list[3]
                spread = None
                if spread_dom:
                    spread = spread_dom.text
                spread_dict = {'pair_name': pair_name, 'spread': spread }
                print(spread_dict)
                #if pair_name == "ドル/円":
                #    bid_dom = pair_name_dom = td_list[1]
                #    bid = bid_dom.text
                #    if bid != lastbid:
                #        #engine.say(lastbid)
                #        engine.say(bid)
                #        engine.runAndWait()
                #        lastbid = bid
        
        self.prev_spread = self.current_spread
        self.current_spread = spread

        return spread


    def update_spread(self):
        spread = None

        target_pair_name = self.get_pair_name_from_pair(self.pair)
        table_div = self.driver.find_element(By.ID, "rate-list-area")
        table = table_div.find_element(By.TAG_NAME, 'table')
        table_html = table.get_attribute('outerHTML')
        soup_table = BeautifulSoup(table_html, features="html.parser")
        tbody = soup_table.find('tbody')
        tr_list = tbody.find_all('tr')

        for tr in tr_list:
            pair_name = None
            th = tr.find('th')
            if th:
                span = th.find('span')
                if span:
                    pair_name = span.text
            
            if target_pair_name == pair_name:
                td_list =  tr.find_all('td')
                spread_dom = td_list[2]
                target_pair_name
                spread = None
                if spread_dom:
                    spread = spread_dom.text
                spread_dict = { 'pair': self.pair, 'pair_name': pair_name, 'spread': spread, 'publisher': 'rakuten' }
                if self.logging:
                    print(spread_dict)
                #if pair_name == "ドル/円":
                #    bid_dom = pair_name_dom = td_list[1]
                #    bid = bid_dom.text
                #    if bid != lastbid:
                #        #engine.say(lastbid)
                #        engine.say(bid)
                #        engine.runAndWait()
                #        lastbid = bid
        
        self.prev_spread = self.current_spread
        self.current_spread = spread

        return spread

    #"https://www.rakuten-sec.co.jp/smartphone/fx/charm/commission.html"
    def get_spread_list_old(self):
        spread_list = []

        table_div = self.driver.find_element(By.ID, "rate-list-area")
        table = table_div.find_element(By.TAG_NAME, 'table')
        table_html = table.get_attribute('outerHTML')
        soup_table = BeautifulSoup(table_html, features="html.parser")
        tbody = soup_table.find('tbody')
        tr_list = tbody.find_all('tr')
        for tr in tr_list:
            td_list =  tr.find_all('td')
            pair_name_dom = td_list[0]
            pair_name = None
            if pair_name_dom:
                pair_name = pair_name_dom.text
            spread_dom = td_list[3]
            spread = None
            if spread_dom:
                spread = spread_dom.text
            spread_dict = { 'pair': self.pair, 'pair_name': pair_name, 'spread': spread, 'publisher': 'rakuten' }
            if self.logging:
                    print(spread_dict)
            spread_list.append(spread_dict)
    
        return spread_list

    def get_spread_list(self):
        spread_list = []

        table_div = self.driver.find_element(By.ID, "rate-list-area")
        table = table_div.find_element(By.TAG_NAME, 'table')
        table_html = table.get_attribute('outerHTML')
        soup_table = BeautifulSoup(table_html, features="html.parser")
        tbody = soup_table.find('tbody')
        tr_list = tbody.find_all('tr')
        for tr in tr_list:
            pair_name = None
            th = tr.find('th')
            if th:
                span = th.find('span')
                if span:
                    pair_name = span.text
            td_list =  tr.find_all('td')
            spread_dom = td_list[2]
            spread = None
            if spread_dom:
                spread = spread_dom.text
            spread_dict = { 'pair': self.pair, 'pair_name': pair_name, 'spread': spread, 'publisher': 'rakuten' }
            if self.logging:
                print(spread_dict)
            spread_list.append(spread_dict)
    
        return spread_list
