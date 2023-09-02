from abc import ABCMeta, abstractmethod


class SpreadsHandler(metaclass=ABCMeta):
    def __init__(self, pair, logging):
        self.pair = pair
        self.logging = logging
        self.prev_spread = None
        self.current_spread = None
        self.driver = self._generate_driver()
    

    @abstractmethod
    def _generate_driver(self):
        pass

    @abstractmethod
    def update_spread(self):
        pass

    @abstractmethod
    def get_spread_list(self):
        pass

    def is_spread_changed(self):
        return self.prev_spread != self.current_spread

    def get_spread(self):
        return self.current_spread
    
    def get_spread_for_anounce(self):
        str_spread = str(self.current_spread)
        spread_for_anounce = ""
        if str_spread.startswith("0."):
            spread_for_anounce = spread_for_anounce + "0."
            str_spread_tail = str_spread[2:]
            str_spread_tail.replace('0', 'まる')
            spread_for_anounce = spread_for_anounce + str_spread_tail
        else:
            str_spread.replace('0', 'まる')
            spread_for_anounce = str_spread
        return spread_for_anounce

    def get_spread_for_anounce_from(self, spread):
        str_spread = str(spread)
        spread_for_anounce = ""
        if str_spread.startswith("0."):
            spread_for_anounce = spread_for_anounce + "0."
            str_spread_tail = str_spread[2:]
            str_spread_tail = str_spread_tail.replace('0', 'まる')
            spread_for_anounce = spread_for_anounce + str_spread_tail
        else:
            str_spread = str_spread.replace('0', 'まる').replace('.', 'てん')
            spread_for_anounce = str_spread
        return spread_for_anounce
    
    def quit_driver(self):
        self.driver.quit()

