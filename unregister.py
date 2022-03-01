import urllib.request
import urllib.error
import json
import pprint
import settings
import variables


def unregister_watch():
    obj = {"Symbols": [
                {'Symbol': settings.symbol, 'Exchange': settings.exchange}
        ]}
    json_data = json.dumps(obj).encode('utf8')

    url = 'http://localhost:' + settings.port + '/kabusapi/unregister'
    req = urllib.request.Request(url, json_data, method='PUT')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', variables.token)

    try:
        print('###unregister')
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            pprint.pprint(content)

    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)
