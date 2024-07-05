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

class GaitameSpreadsHandler(SpreadsHandler):
    def __init__(self, pair, logging):
        super().__init__(pair, logging)

    def _generate_driver(self):
        print("generate gaitame driver")
        url = "https://www.gaitame.com/markets/rate/"
        r = requests.get(url, params={})
        if r.status_code != 200:
            raise ValueError("can not connect to gaitame data source," + str(r.status_code))
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        #options.headless = True
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.get(url)

        return self.driver

    def update_spread(self):
        spread = None

        table_div = self.driver.find_element(By.ID, "rate-table")
        table = table_div.find_element(By.TAG_NAME, 'table')
        table_html = table.get_attribute('outerHTML')
        soup_table = BeautifulSoup(table_html, features="html.parser")
        tbody = soup_table.find('tbody')
        tr_list = tbody.find_all('tr', attrs={'class': 'rateCurr'})

        for tr in tr_list:
            if not tr.has_attr('class'):
                print("can not get pair name")
                continue
            pair = tr['class'][0]

            if pair == self.pair:
                pair_name_dom = tr.find('a')
                pair_name = None
                if pair_name_dom:
                    pair_name_dom.span.clear()
                    pair_name = pair_name_dom.text
                spread_dom = tr.find('td', attrs={'class': 'spread'})
                if spread_dom:
                    spread = spread_dom.text
                spread_dict = {'pair': pair, 'pair_name': pair_name, 'spread': spread, 'publisher': 'gaitame' }
                if self.logging:
                    print(spread_dict)
        
        self.prev_spread = self.current_spread
        self.current_spread = spread

        return spread


    def get_spread_list(self):
        spread_list = []

        table_div = self.driver.find_element(By.ID, "rate-table")
        table = table_div.find_element(By.TAG_NAME, 'table')
        table_html = table.get_attribute('outerHTML')
        soup_table = BeautifulSoup(table_html, features="html.parser")
        tbody = soup_table.find('tbody')
        tr_list = tbody.find_all('tr', attrs={'class': 'rateCurr'})

        for tr in tr_list:
            if not tr.has_attr('class'):
                print("can not get pair name")
                continue
            pair = tr['class'][0]
            pair_name_dom = tr.find('a')
            pair_name = None
            if pair_name_dom:
                pair_name_dom.span.clear()
                pair_name = pair_name_dom.text
            spread_dom = tr.find('td', attrs={'class': 'spread'})
            spread = None
            if spread_dom:
                spread = spread_dom.text
            spread_dict = {'pair': pair, 'pair_name': pair_name, 'spread': spread, 'publisher': 'gaitame' }
            if self.logging:
                print(spread_dict)
            spread_list.append(spread_dict)
    
        return spread_list
