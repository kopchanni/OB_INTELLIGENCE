import requests
from binance.client import Client
import pandas as pd
base_url_kucoin = 'https://api.kucoin.com'
binance_url_base = ''
binance_api = ''
binance_secret = ''


class BinanceClient:
    def __init__(self, apiKey: str, apiSecret: str, testnet: bool):
        if testnet:
            self._base_url = "https://testnet.binancefuture.com"
            self.wss_url =  "wss://stream.binancefuture.com/ws"
        else:
            self.base_url = "https://api.binance.com"
        self._apiKey = apiKey
        self._apiSecret = apiSecret
        self.connection = Client(api_key=self._apiKey,api_secret=self._apiSecret)
        self.orderbook = dict()

        self.logs = []

    def orderbook_data_manipulation(self, pair: str):
        pair_price_ask = []
        pair_price_bid = []
        pair_quantity_ask = []
        pair_quantity_bid = []
        expected_volume_ask = []
        expected_volume_bid = []

        depth = self.connection.get_order_book(symbol=f'{pair}')
        ask = depth['asks']
        bid = depth['bids']

        # mainpulate list to extract $ & qty
        for row in ask:
            for col in row:
                for x in row:
                    price = row[0]
                    quantity = row[1]
                    pair_price_ask.append(price)
                    pair_quantity_ask.append(quantity)
                    price_qty_vol = float(float(price) * float(quantity))
                    expected_volume_ask.append(price_qty_vol)

        for row in bid:
            for col in row:
                for x in row:
                    price = row[0]
                    quantity = row[1]
                    pair_price_bid.append(price)
                    pair_quantity_bid.append(quantity)
                    price_qty_vol = float(float(price) * float(quantity))
                    expected_volume_bid.append(price_qty_vol)
       
        '''
        OB STATS PRICE & QUANTITY
        '''
        
        print('--------------------------------------------------------------------------------------------------')
        mean_ask_price_ser = pd.Series(pair_price_ask).astype('float')
        median_ask_price_ser = pd.Series(pair_price_ask).astype('float')
        std_ask_price_ser = pd.Series(pair_price_ask).astype('float')
        des_ask_price_ser = pd.Series(pair_price_ask).astype('float')
        ask_price_mean = mean_ask_price_ser.mean()
        ask_price_med = median_ask_price_ser.median()
        ask_price_std = std_ask_price_ser.std()
        ask_price_des = des_ask_price_ser.describe()
        print("MEAN ASK PRICE", ask_price_mean)
        print("MEDIAN ASK PRICE", ask_price_med)
        print('STANDARD DEVIATION', ask_price_std)
        print("CURRENT ORDERBOOK STATS: $")
        print(ask_price_des)
        print('--------------------------------------------------------------------------------------------------')
        meanpair_quantity_ask_ser = pd.Series(pair_quantity_ask).astype('float')
        medianpair_quantity_ask_ser = pd.Series(pair_quantity_ask).astype('float')
        stdpair_quantity_ask_ser = pd.Series(pair_quantity_ask).astype('float')
        despair_quantity_ask_ser = pd.Series(pair_quantity_ask).astype('float')
        pair_quantity_ask_mean = meanpair_quantity_ask_ser.mean()
        pair_quantity_ask_med = medianpair_quantity_ask_ser.median()
        pair_quantity_ask_std = stdpair_quantity_ask_ser.std()
        ask_price_des = despair_quantity_ask_ser.describe()
        print("MEAN ASK QTY",pair_quantity_ask_mean)
        print("MEDIAN ASK QTY",pair_quantity_ask_med)
        print('STANDARD DEVIATION',pair_quantity_ask_std)
        print('CURRENT ORDERBOOK STATS: QTY')
        print(ask_price_des)
        print('--------------------------------------------------------------------------------------------------')
        mean_bid_price_ser = pd.Series(pair_price_bid).astype('float')
        median_bid_price_ser = pd.Series(pair_price_bid).astype('float')
        std_bid_price_ser = pd.Series(pair_price_bid).astype('float')
        des_bid_price_ser = pd.Series(pair_price_bid).astype('float')
        bid_price_mean = mean_bid_price_ser.mean()
        bid_price_med = median_bid_price_ser.median()
        bid_price_std = std_bid_price_ser.std()
        bid_price_des = des_bid_price_ser.describe()
        print("MEAN BID PRICE", bid_price_mean)
        print("MEDIAN BID PRICE", bid_price_med)
        print('STANDARD DEVIATION', bid_price_std)
        print("CURRENT ORDERBOOK STATS: $")
        print(bid_price_des)
        print('--------------------------------------------------------------------------------------------------')
        meanpair_quantity_bid_ser = pd.Series(pair_quantity_bid).astype('float')
        medianpair_quantity_bid_ser = pd.Series(pair_quantity_bid).astype('float')
        stdpair_quantity_bid_ser = pd.Series(pair_quantity_bid).astype('float')
        despair_quantity_bid_ser = pd.Series(pair_quantity_bid).astype('float')
        pair_quantity_bid_mean = meanpair_quantity_bid_ser.mean()
        pair_quantity_bid_med = medianpair_quantity_bid_ser.median()
        pair_quantity_bid_std = stdpair_quantity_bid_ser.std()
        bid_price_des = despair_quantity_bid_ser.describe()
        print("MEAN BID QTY", pair_quantity_bid_mean)
        print("MEDIAN BID QTY", pair_quantity_bid_med)
        print('STANDARD DEVIATION', pair_quantity_bid_std)
        print('CURRENT ORDERBOOK STATS: QTY')
        print(bid_price_des)
        print('==================================================================================================')
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

        horizontal_df_stack = pd.concat([exp_OBVOL_ask_df,exp_OBVOL_bid_df], axis=1)
        horizontal_df_stack.dropna()
        #print(horizontal_df_stack)
        print('==================================================================================================')


   def recent_trade_stats(self, symbol: str):
        sell_trades_price_list = []
        sell_trades_qty_list = []
        buy_trades_price_list = []
        buy_trades_qty_list = []
        trades= self.connection.get_recent_trades(symbol=symbol)
        # {'id': 333420296, 'price': '39659.94000000', 'qty': '0.03831000',
        # 'quoteQty': '1519.37230140','time': 1649723895180,
        # 'isBuyerMaker': True, 'isBestMatch': True},
        for trade in trades:
            if trade['isBuyerMaker']:
                price_trade = trade['price']
                qty_trade = trade['qty']
                buy_trades_price_list.append(price_trade)
                buy_trades_qty_list.append(qty_trade)
            elif trade['isBuyerMaker'] == False:
                price_trade = trade['price']
                qty_trade = trade['qty']
                sell_trades_price_list.append(price_trade)
                sell_trades_qty_list.append(qty_trade)
        print('========================================================================')
        sell_price = pd.Series(sell_trades_price_list).astype('float')
        sell_qty = pd.Series(sell_trades_qty_list).astype('float')
        
        print('MEAN SELL PRICE $: ', sell_price.mean())
        print('MEAN SELL QTY : ', sell_qty.mean())
        buy_price = pd.Series(buy_trades_price_list).astype('float')
        buy_qty = pd.Series(buy_trades_qty_list).astype('float')

        print('MEAN BUY PRICE $: ', buy_price.mean())
        print('MEAN BUY QTY : ', buy_qty.mean())
        sum_sell = sell_price.mean() * sell_qty.sum()
        sum_buy = buy_price.mean() * buy_qty.sum()
        print('TOTAL SELL VOLUME $: ', sum_sell)
        print('TOTAL BUY VOLUME $: ', sum_buy)
        print('------------------------------------------------------------------------')
        # if sum_buy > sum_sell:
        #     print("BULLS MARKET")
        # elif sum_buy < sum_sell:
        #     print('BEAR MARKET')
        print('========================================================================')
        print('RECENT TRADES STATS: SELL')
        print(sell_price.describe())
        print(sell_qty.describe())
        print('RECENT TRADE STATS: BUY')
        print(buy_price.describe())
        print(buy_qty.describe())
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    binance_read = BinanceClient(apiKey=binance_api,apiSecret=binance_secret, testnet=False)
    binance_read.orderbook_stats(pair='BTCBUSD')
    binance_read.recent_trade_stats(symbol='BTCBUSD')






    # print(df)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
