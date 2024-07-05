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

class MinFxSpreadsHandler(SpreadsHandler):
    def __init__(self, pair, logging):
        super().__init__(pair, logging)

    def get_pair_name_from_pair(self, pair):
        pair_name_dict = {
            "usdjpy": "USDJPY",
            "eurjpy": "EURJPY",
            "gbpjpy": "GBPJPY",
            "audjpy": "AUDJPY",
            "nzdjpy": "NZDJPY",
        }
        pair_name = pair_name_dict[pair]
        
        return pair_name

    def _generate_driver(self):
        print("generate minfx driver")
        #if self.driver:
        #    print("driver is already exist!")
        #    return
        url = "https://min-fx.jp/market/rate/"
        r = requests.get(url, params={})
        if r.status_code != 200:
            raise ValueError("can not connect to minfx data source," + str(r.status_code))
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        #options.headless = True
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.get(url)

        return self.driver

    def update_spread(self):
        spread = None

        target_pair_name = self.get_pair_name_from_pair(self.pair)
        table_div = self.driver.find_element(By.ID, "mainbody")
        table = table_div.find_element(By.TAG_NAME, 'table')
        table_html = table.get_attribute('outerHTML')
        soup_table = BeautifulSoup(table_html, features="html.parser")
        #id=ratetabledata
        tbody = soup_table.find('tbody')
        tr_list = tbody.find_all('tr')

        for tr in tr_list:
            td_list =  tr.find_all('td')
            pair_name_dom = td_list[0]
            pair_name = None
            if pair_name_dom and pair_name_dom.img and pair_name_dom.img.get("alt"):
                pair_name = pair_name_dom.img.get("alt")
            
            if target_pair_name == pair_name:
                spread = None
                spread_dom = td_list[6]
                if spread_dom:
                    spread = spread_dom.text
                    spread_dict = { 'pair': self.pair, 'pair_name': pair_name, 'spread': spread, 'publisher': 'minfx' }
                    if self.logging:
                        print(spread_dict)
        
        self.prev_spread = self.current_spread
        self.current_spread = spread

        return spread

    def get_spread_list(self):
        spread_list = []

        #target_pair_name = self.get_pair_name_from_pair(self.pair)
        table_div = self.driver.find_element(By.ID, "mainbody")
        table = table_div.find_element(By.TAG_NAME, 'table')
        table_html = table.get_attribute('outerHTML')
        soup_table = BeautifulSoup(table_html, features="html.parser")
        #id=ratetabledata
        tbody = soup_table.find('tbody')
        tr_list = tbody.find_all('tr')

        for tr in tr_list:
            td_list =  tr.find_all('td')
            pair_name_dom = td_list[0]
            pair_name = None
            if pair_name_dom and pair_name_dom.img and pair_name_dom.img.get("alt"):
                pair_name = pair_name_dom.img.get("alt")

            spread_dom = td_list[6]
            if spread_dom:
                    spread = spread_dom.text
                    spread_dict = { 'pair': self.pair, 'pair_name': pair_name, 'spread': spread, 'publisher': 'minfx' }
                    if self.logging:
                        print(spread_dict)
                        spread_list.append(spread_dict)
    
        return spread_list
