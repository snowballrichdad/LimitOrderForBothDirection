import pprint
import json

import send_order_exit
import settings
import variables
import datetime
import websocket
import sys
import positions


class WebsocketExitC:

    def __init__(self):
        self.isException = True

    def on_message(self, ws, message):
        self.print_with_time('--- RECV MSG. --- ')
        content = json.loads(message)
        symbol = content["Symbol"]
        if symbol != settings.symbol:
            return

        cur_price = content["CurrentPrice"]

        if cur_price is None:
            return

        pprint.pprint("curPrice:" + str(cur_price))
        pprint.pprint("orderPrice:" + str(variables.order_price))

        # 損切り
        if settings.side == 1:
            if cur_price >= variables.order_price + settings.loss_cut_margin:
                self.send_order_market(ws)
        else:
            if cur_price <= variables.order_price - settings.loss_cut_margin:
                self.send_order_market(ws)

        # 利食い
        if settings.side == 1:
            if cur_price <= variables.order_price - settings.take_profit_margin:
                self.send_order_ioc_limit(ws, cur_price)
        else:
            if cur_price >= variables.order_price + settings.take_profit_margin:
                self.send_order_ioc_limit(ws, cur_price)

    def send_order_market(self, ws):
        # 成行
        send_order_exit.send_order_market()

        self.isException = False
        ws.close()

    def send_order_ioc_limit(self, ws, price):
        # IOC指値
        send_order_exit.send_order_ioc_limit(price)

        # 建玉数を更新
        positions.get_positions()

        # 建玉がなくなったら終了
        if variables.exitQty == 0:
            self.isException = False
            ws.close()

    def on_error(self, ws, error):
        if len(error) != 0:
            self.print_with_time('--- ERROR --- ')
            print(error)

    def on_close(self, ws):
        self.print_with_time('--- DISCONNECTED --- ')

    def on_open(self, ws):
        self.print_with_time('--- CONNECTED --- ')

    def stat_push_api_client(self):
        self.print_with_time('--- webSocket_exit Start--- ')
        url = 'ws://localhost:' + settings.port + '/kabusapi/websocket'
        # websocket.enableTrace(True)
        ws = websocket.WebSocketApp(url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()

        self.print_with_time('--- websocket_exit --- ')

        if self.isException:
            print("exit")
            sys.exit()

    @staticmethod
    def print_with_time(message):
        print(str(datetime.datetime.now()) + ' ' + message)
