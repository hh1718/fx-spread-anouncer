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

class GaikaexSpreadsHandler(SpreadsHandler):
    def __init__(self, pair, logging):
        super().__init__(pair, logging)

    def _generate_driver(self):
        print("generate gaikaex driver")
        #if self.driver:
        #    print("driver is already exist!")
        #    return
        #url = "https://www.gaikaex.com/gaikaex/mark/all_price_board.html"
        url = "https://www.gaikaex.com/gaikaex/mark/rate_board_new.html"
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

    def update_spread(self):
        spread = None

        table_div = self.driver.find_element(By.ID, "ratebox")
        table_html = table_div.get_attribute('outerHTML')
        soup_table = BeautifulSoup(table_html, features="html.parser")
        table_list_wrap = soup_table.find('ul', attrs={'id': 'jquery-ui-sortable'})
        table_list = table_list_wrap.find_all('li', attrs={'class': 'ui-state-default'})

        for table_wrap in table_list:
            tr = table_wrap.find('tr')
            if not tr.has_attr('class'):
                print("no tr")
                continue
            pair = tr['class'][0]
            if pair == self.pair:
                td_list = tr.find_all('td')
                pair_name = None

                if len(td_list) >= 0:
                    pair_name_dom = td_list[0]
                    if pair_name_dom:
                        pair_name = pair_name_dom.text
                    spread_dom = td_list[3]
                    if spread_dom:
                        spread_p = spread_dom.find('p')
                        if spread_p:
                            spread = spread_p.text
                spread_dict = {'pair': pair, 'pair_name': pair_name, 'spread': spread, 'publisher': 'gaikaex' }
                if self.logging:
                    print(spread_dict)
        self.prev_spread = self.current_spread
        self.current_spread = spread

        return spread


    def get_spread_list(self):
        spread_list = []

        table_div = self.driver.find_element(By.ID, "ratebox")
        table_html = table_div.get_attribute('outerHTML')
        soup_table = BeautifulSoup(table_html, features="html.parser")
        table_list_wrap = soup_table.find('ul', attrs={'id': 'jquery-ui-sortable'})
        table_list = table_list_wrap.find_all('li', attrs={'class': 'ui-state-default'})

        for table_wrap in table_list:
            tr = table_wrap.find('tr')
            if not tr.has_attr('class'):
                print("no tr")
                continue
            pair = tr['class'][0]
            td_list = tr.find_all('td')
            pair_name = None
            spread = None

            if len(td_list) >= 0:
                pair_name_dom = td_list[0]
                if pair_name_dom:
                    pair_name = pair_name_dom.text

                spread_dom = td_list[3]
                if spread_dom:
                    spread_p = spread_dom.find('p')
                    if spread_p:
                        spread = spread_p.text

            spread_dict = {'pair': pair, 'pair_name': pair_name, 'spread': spread , 'publisher': 'gaikaex'}
            if self.logging:
                print(spread_dict)
            spread_list.append(spread_dict)
    
        return spread_list
