import urllib.request
import urllib.error
import urllib.parse
import json
import pprint
import settings
import sys
import variables


def get_positions():
    url = 'http://localhost:' + settings.port + '/kabusapi/positions'
    params = {'product': 0, 'symbol': settings.symbol, 'side': settings.side}
    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)), method='GET')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', variables.token)

    try:
        print('###positions')
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            res_json = res.read()
            content = json.loads(res_json)
            pprint.pprint(content)

            # ポジション数を返す
            leaves_qty = 0
            for position in content:

                # 残ポジション数を上書き
                for close_positions_dic in variables.closePositions:
                    if close_positions_dic['HoldID'] == position['ExecutionID']:
                        close_positions_dic['Qty'] = position['LeavesQty']
                        leaves_qty = leaves_qty + position['LeavesQty']

            # 建玉数を更新
            variables.exitQty = leaves_qty
            return

    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)

    sys.exit()
