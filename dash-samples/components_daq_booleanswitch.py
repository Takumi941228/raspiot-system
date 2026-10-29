# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashとDash DAQ（スイッチなどのUI部品）を使用して、
# Webブラウザ上からMQTT経由でデバイス（ESP32など）の動作モードを切り替える
# インタラクティブなWebアプリケーションです。
# 画面上の3つのスイッチ（BooleanSwitch）のいずれかが操作されると、その状態を検知し、
# 対応するモード番号（JSON形式）をMQTTブローカーへ送信します。
# ==============================================================================

# 1. ライブラリ・モジュールの読み込み (インポート)
import paho.mqtt.client as mqtt  # MQTT通信を行うためのPaho MQTTライブラリ
import json                      # Pythonの辞書やデータをJSON形式の文字列に変換するモジュール
import dash_daq as daq           # Dashでスイッチなどの高度なUI部品（BooleanSwitchなど）を使うためのライブラリ

# Webアプリケーション作成用ライブラリ (Dash)
from dash import Dash, html, Input

# 2. MQTT接続設定・パラメータの定義
MQTT_HOST = 'xx.xx.xx.xx'  # 接続先MQTTブローカのIPアドレス
MQTT_PORT = 1883           # MQTT通信ポート
MQTT_TOPIC = 'esp32/mode'  # メッセージを送信するMQTTトピック

# 3. アプリの初期化
# Dashのインスタンス生成
app = Dash()

# 4. ダッシュボードのレイアウト定義 (UI設計)
# 画面上に3つのBooleanSwitch（オン/オフ切り替えスイッチ）を配置します
app.layout = html.Div([
    html.H3("モード切替パネル", style={'fontFamily': 'sans-serif'}),
    
    # スイッチ1〜3（それぞれに一意のIDを付与）
    daq.BooleanSwitch(id='our-boolean-switch1', on=False, label="Mode 0 Switch"),
    daq.BooleanSwitch(id='our-boolean-switch2', on=False, label="Mode 1 Switch"),
    daq.BooleanSwitch(id='our-boolean-switch3', on=False, label="Mode 2 Switch"),
])

# 5. コールバック処理（スイッチ操作連動のMQTT送信）
# いずれかのスイッチが切り替わった（Inputの変化）のを検知して実行されます。
# ※画面上の出力を更新しない、副作用（MQTT送信）を伴うアクションの記述です。
@app.callback(
    Input('our-boolean-switch1', 'on'),
    Input('our-boolean-switch2', 'on'),
    Input('our-boolean-switch3', 'on')
)

def update_output(on1, on2, on3):
    """
    スイッチの状態変化を受け取り、条件に応じてMQTTブローカへモード番号を送信する関数
    """
    # MQTTブローカーへの接続とバックグラウンドループの開始
    connect()
    
    # 各スイッチのオン/オフ状態を判定し、送信するJSONペイロード（モード）を決定
    if on1 == True:
        payload = json.dumps({"mode": 0})
    elif on2 == True:
        payload = json.dumps({"mode": 1})
    else:
        payload = json.dumps({"mode": 2})
    
    # 指定したトピックへMQTTメッセージをQoS 0で送信
    mqttClient.publish(MQTT_TOPIC, payload, qos=0)
    
    # 送信完了後、MQTTのループを停止して切断
    mqttClient.loop_stop()
    mqttClient.disconnect()

# 6. MQTT接続・通信用の補助関数
def connect():
    """
    MQTTクライアントを初期化し、ブローカーへの接続とバックグラウンド送受信を開始する関数
    """
    global mqttClient
    mqttClient = mqtt.Client()

    # MQTTブローカーに接続する（タイムアウト120秒）
    mqttClient.connect(MQTT_HOST, MQTT_PORT, 120)

    # データの送受信ループ（バックグラウンドスレッド）を開始する
    mqttClient.loop_start()

# 7. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8050, debug=False)