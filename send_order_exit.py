import urllib.request
import urllib.error
import json
import pprint
import settings
import variables
import sys


class SendOrderExitBase:

    def __init__(self):

        self.obj = {'Password': settings.password,
                    'Symbol': settings.symbol,
                    'Exchange': settings.exchange,
                    'SecurityType': 1,
                    'Side': settings.opposite_side,
                    'CashMargin': 3,
                    'MarginTradeType': settings.margin_trade_type,
                    'DelivType': settings.closing_deliv_type,
                    'AccountType': settings.account_type,
                    'Qty': variables.exitQty,
                    'ClosePositions': variables.closePositions,
                    'Price': 0,
                    'ExpireDay': 0,
                    'FrontOrderType': 10}

    def send_order(self):
        json_data = json.dumps(self.obj).encode('utf-8')

        url = 'http://localhost:' + settings.port + '/kabusapi/sendorder'
        req = urllib.request.Request(url, json_data, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('X-API-KEY', variables.token)

        try:
            print('###send_order_exit')
            with urllib.request.urlopen(req) as res:
                print(res.status, res.reason)
                for header in res.getheaders():
                    print(header)
                print()
                content = json.loads(res.read())
                pprint.pprint(content)

                return

        except urllib.error.HTTPError as e:
            print(e)
            content = json.loads(e.read())
            pprint.pprint(content)
            # 決済内容に誤りがあります はポジション取得遅延のせいなので無視
            if content['Code'] == 8:
                return

        except Exception as e:
            print(e)

        sys.exit()


class MarketSendOrderExit(SendOrderExitBase):

    def __init__(self):
        super().__init__()

    def send_order_market(self):
        print('###send_order_market')
        self.obj["FrontOrderType"] = 10
        self.obj["Price"] = 0
        super().send_order()


class IOCLimitSendOrderExit(SendOrderExitBase):

    def __init__(self):
        super().__init__()

    def send_order_ioc_limit(self, price):
        print('###send_order_ioc_limit')
        self.obj["FrontOrderType"] = 27
        self.obj["Price"] = price
        super().send_order()


def send_order_market():
    temp_class = MarketSendOrderExit()
    temp_class.send_order_market()


def send_order_ioc_limit(price):
    temp_class = IOCLimitSendOrderExit()
    temp_class.send_order_ioc_limit(price)
