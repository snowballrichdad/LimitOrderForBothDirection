import settings
import get_token
import register
import send_order_entry
import order_info
import websocket_exit
import unregister
import time

# トークン取得
get_token.token()

# PUSH API銘柄登録
register.register()
# 新規建て発注
send_order_entry.send_order()

# すべてエントリできるまで待つ
while True:
    # 新規建て発注情報取得
    if order_info.orders_info():
        break
    time.sleep(settings.settlement_check_interval)

# PUSH APIで価格監視開始
wsk_ext = websocket_exit.WebsocketExitC()
wsk_ext.stat_push_api_client()

# PUSH API銘柄登録解除
unregister.unregister_watch()
