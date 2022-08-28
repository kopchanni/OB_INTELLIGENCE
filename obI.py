import datetime
from binance.client import Client
import pandas as pd
from binance.exceptions import *
import time
import datetime as dt

# binance websocket address
binance_wss_address = 'wss://stream.binance.com:9443'


class BinanceReadOnlyClient:
    def __init__(self, apiKey: str, apiSecret: str, testnet: bool):
        if testnet:
            self._base_url = "https://testnet.binancefuture.com"
            self.wss_url = "wss://stream.binancefuture.com/ws"
        else:
            self.base_url = "https://api.binance.com"
        self._apiKey = apiKey
        self._apiSecret = apiSecret
        self.connection = Client(api_key=self._apiKey, api_secret=self._apiSecret)
        self.orderbook = dict()
        self.argtrades = dict()
        self.logs = []

    def API_info_stats(self):
        # binance.exceptions.BinanceAPIException:
        try:
            status = self.connection.get_account()
            print(status)
        except BinanceAPIException as e:
            print(e)

    def get_realTime_price(self, symbol:str, interval:str):
        data = self.connection.get_klines(symbol=symbol, interval=interval)
        print(data)
        open = data[1]
        high = data[2]
        low = data[3]
        close = data[4]
        volume = data[5]
        num_trades = data[8]
        buyer_vol = data[9]
        seller_vol = data[10]
        print(volume)


    def orderbook_reformat(self, pair:str):
        pair_price_ask = []
        pair_price_bid = []
        pair_quantity_ask = []
        pair_quantity_bid = []
        expected_volume_ask = []
        expected_volume_bid = []
        current_time_list = []
        print("RECIVING ORDERBOOK DATA")

        depth = self.connection.get_order_book(symbol=f'{pair}')

        # price = self.connection.
        ask = depth['asks']
        bid = depth['bids']

        # mainpulate list to extract $ & qty
        print('EXTRACTING DATA')
        for row in ask:
            for col in row:
                for x in row:
                    price = row[0]
                    quantity = row[1]
                    pair_price_ask.append(price)
                    pair_quantity_ask.append(quantity)
                    price_qty_vol = float(float(price) * float(quantity))
                    expected_volume_ask.append(price_qty_vol)
                    now = datetime.datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    current_time_list.append(current_time)

        for row in bid:
            for col in row:
                for x in row:
                    price = row[0]
                    quantity = row[1]
                    pair_price_bid.append(price)
                    pair_quantity_bid.append(quantity)
                    price_qty_vol = float(float(price) * float(quantity))
                    expected_volume_bid.append(price_qty_vol)
                    now = datetime.datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    current_time_list.append(current_time)

        # now = datetime.datetime.now()
        # current_time = now.strftime("%H:%M:%S")
        time_ser = pd.Series(current_time_list)
        ask_ser = pd.Series(pair_price_ask)
        quantity_ask_ser = pd.Series(pair_quantity_ask).astype('float')
        median_ask_price_ser = pd.Series(pair_price_ask)
        std_ask_price_ser = pd.Series(pair_price_ask)
        des_ask_price_ser = pd.Series(pair_price_ask)

        bid_ser = pd.Series(pair_price_bid).astype('float')
        quantity_bid_ser = pd.Series(pair_quantity_bid)
        median_bid_price_ser = pd.Series(pair_price_bid).astype('float')
        std_bid_price_ser = pd.Series(pair_price_bid).astype('float')
        des_bid_price_ser = pd.Series(pair_price_bid).astype('float')

        # # EXPECTED VOLUME OF ORDERS PLACED
        expected_OBVOL_ask = pd.Series(expected_volume_ask)
        expected_OBVOL_bid = pd.Series(expected_volume_bid)

        dict_data = {'pair_ask':ask_ser, 'pair_bid':bid_ser,'quantity_ask':quantity_ask_ser,
                     'quantity_bid': quantity_bid_ser, 'expected_volume_ask':expected_OBVOL_ask,
                     'expected_volume_bid':expected_OBVOL_bid}
        # df_OB = pd.concat([ask_ser,bid_ser,quantity_ask_ser,quantity_bid_ser,expected_OBVOL_ask,expected_OBVOL_bid],
        #                   axis=1)
        df_OB = pd.DataFrame(data=dict_data).round(decimals=2)

        return df_OB

    def orderbook_stats(self, pair: str):

        df_OB = self.orderbook_reformat(pair=f'{pair}')

        # print(df_OB)
        '''

        AVR PRICE & QUANTITY

        '''
        df_OB['pair_ask'] = pd.to_numeric(df_OB['pair_ask'], downcast='float')
        df_OB['pair_bid'] = pd.to_numeric(df_OB['pair_bid'], downcast='float')
        df_OB['quantity_ask'] = pd.to_numeric(df_OB['quantity_ask'], downcast='float')
        df_OB['quantity_bid'] = pd.to_numeric(df_OB['quantity_bid'], downcast='float')

        # avg price ask
        print('--------------------------------------------------------------------------------------------------')
        #
        #
        ask_price_ser = pd.Series(df_OB['pair_ask'])

        #
        ask_price_mean = ask_price_ser.mean()

        ask_price_med = ask_price_ser.median()
        # ask_price_std = std_ask_price_ser.std(ddof=2)
        ask_price_des = ask_price_ser.describe()
        #
        #
        print('=============================================================================')
        print("MEAN ASK PRICE", ask_price_mean)
        print("MEDIAN ASK PRICE", ask_price_med)
        print('ASK PRICE STATS', ask_price_des)
        print('=============================================================================')
        # print('STANDARD DEVIATION', ask_price_std)
        # print("CURRENT ORDERBOOK STATS: $")
        #
        # # print(ask_price_des)
        # print('--------------------------------------------------------------------------------------------------')
        #
        qty_ask_ser = pd.Series(df_OB['quantity_ask'])
        quantity_ask_mean = qty_ask_ser.mean()
        pair_quantity_ask_med = qty_ask_ser.median()
        # pair_quantity_ask_std = stdpair_quantity_ask_ser.std(ddof=2)
        ask_qty_des = qty_ask_ser.describe()
        #
        print("MEAN ASK QTY", quantity_ask_mean)
        print("MEDIAN ASK QTY", pair_quantity_ask_med)
        print("ASK PRICE QTY STATS ", ask_qty_des)
        print('=============================================================================')

        #
        # print('--------------------------------------------------------------------------------------------------')
        #

        #
        bid_ser = pd.Series(df_OB['pair_bid'])
        bid_price_mean = bid_ser.mean()
        bid_price_med = bid_ser.median()
        # bid_price_std = std_bid_price_ser.std(ddof=2)
        bid_price_des = bid_ser.describe()
        print('=============================================================================')
        print("MEAN BID PRICE", bid_price_mean)
        print("MEDIAN BID PRICE", bid_price_med)
        print('BID PRICE STATS', bid_price_des)
        print('=============================================================================')

        #
        qty_bid_ser = pd.Series(df_OB['quantity_bid'])
        quantity_bid_mean = qty_bid_ser.mean()
        quantity_bid_med = qty_bid_ser.median()
        # pair_quantity_bid_std = stdpair_quantity_bid_ser.std(ddof=2)
        bid_qty_des = qty_bid_ser.describe()
        #
        print('==================================================================================================')
        print("MEAN BID QTY", quantity_bid_mean)
        print("MEDIAN BID QTY", quantity_bid_med)
        print('QTY BID STATS', bid_qty_des)
        print('==================================================================================================')


        """
            Difference
        """

        print('DIFFERENCE (ask - bid) mean')
        diff = ask_price_mean - bid_price_mean
        print(diff, ' $')
        print(bid_price_mean+diff)
        print('QTY DIFFERENCE')
        print(quantity_bid_mean-quantity_ask_mean)

        print('DIFFERENCE (ask - bid) med')
        diff_2 = ask_price_med - bid_price_med
        print(diff_2, ' $')
        # spread == difference
        # more spread meaning low liquidity; slow time for price action
        # less spread meaning higher liquidity; faster price action
        print('=============================================================================')
        total_vol_ask = df_OB['expected_volume_ask'].sum()
        total_vol_bid = df_OB['expected_volume_bid'].sum()
        #
        if total_vol_ask > total_vol_bid:
            print('CURRENT OB BOOKED AT SELLING')
            print('SELLING BOOKED VOLUME: ', total_vol_ask)
            print('BUYING BOOKED VOLUME: ', total_vol_bid)
            print('==================================================================================================')
        elif total_vol_bid > total_vol_ask:
            print('CURRENT OB BOOKED AT BUYING')
            print('BUYING BOOKED VOLUME: ', total_vol_bid)
            print('SELLING BOOKED VOLUME: ', total_vol_ask)
            print('==================================================================================================')
        elif total_vol_bid == total_vol_ask:
            print('CURRENT OB BOOKED AT NEURAL')
            print('BUYING BOOKED VOLUME: ', total_vol_bid)
            print('SELLING BOOKED VOLUME: ', total_vol_ask)
            print('==================================================================================================')


   
