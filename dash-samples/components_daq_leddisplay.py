# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashとDash DAQのLEDディスプレイ（daq.LEDDisplay）を使用して、
# 指定したセンサーノードの温度・湿度・気圧の最新データを定期的に取得し、
# デジタル数字形式でリアルタイム（5秒ごと）に表示するWebアプリケーションです。
# ユーザは起動時にターミナルから対象ノードIDとサンプル数を入力します。
# ==============================================================================

# 1. ライブラリ・モジュールの読み込み (インポート)
# DB関連をまとめたモジュール（自作モジュール：DBへの接続やデータ取得関数を管理）
import db_ambient_count02

# グラフ表示に関するライブラリ（データフレームという表形式でデータを扱うためのPandas）
import pandas as pd

# グラフ描画用ライブラリ（Plotly Express）
import plotly.express as px

# DashでLED風のデジタル表示器などの高度なUI部品を使うためのライブラリ
import dash_daq as daq

# Webアプリケーション作成用ライブラリ (Dash)
# - Dash: アプリケーション本体
# - dcc (Dash Core Components): タイマ（Interval）などのUI部品
# - html (Dash HTML Components): HTMLタグ（枠組みなど）を作成する部品
# - Output, Input: 画面を動的に更新するための仕組み
from dash import Dash, dcc, html, Output, Input

# 2. アプリの初期化と起動時パラメータの設定
# アプリの初期化
app = Dash()

# クエリのパラメータをターミナルから入力
print('最新のデータを表示します。')
print('どのノードのデータを表示しますか？')
node_id = input('ノードの Identifier (例: tochigi_mqtt_0XX): ')

print('何サンプル前のデータまで表示しますか？')
# 入力したデータを数値（整数）に変換
limit_count = int(input('数値を入力 (例: 10) : '))

# 3. ダッシュボードのレイアウト定義 (UI設計)
# 画面上に3つのLEDDisplay（温度・湿度・気圧）と、自動更新用のタイマを配置します
app.layout = html.Div([
    # 【自動更新タイマ】指定したミリ秒ごとにコールバックを呼び出す（例: 5000ms = 5秒ごと）
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # 更新間隔（ミリ秒）
        n_intervals=0       # 起動からの経過カウント
    ),
    
    # 【LEDディスプレイ部品】温度、湿度、気圧をデジタル数字で表示
    daq.LEDDisplay(
        id='our-LED-display1',
        label="Temp [deg.C]",
        value="0",
        size=30
    ),
    daq.LEDDisplay(
        id='our-LED-display2',
        label="Humi [%]",
        value="0",
        size=30
    ),
    daq.LEDDisplay(
        id='our-LED-display3',
        label="Press [hPa]",
        value="0",
        size=30
    ),
])

# 4. コールバック処理（定期的なデータ取得とLEDの更新）
# タイマ（dcc.Interval）が一定時間ごとに進む（Inputの変化）のを検知して実行されます。
@app.callback(
    Output('our-LED-display1', 'value'),
    Output('our-LED-display2', 'value'),
    Output('our-LED-display3', 'value'),
    Input('interval-component', 'n_intervals')  # タイマのカウント変化をトリガーにする
)
def update_output(n_intervals):
    """
    タイマーの時間が来るたびに実行される関数。
    データベースから最新データを取得し、各LEDディスプレイの値を文字列に変換して返します。
    """
    # 1. データベースサーバに接続
    db_ambient_count02.connect()

    # 2. 指定されたノードIDと件数条件で最新データをクエリ（検索実行）
    result = db_ambient_count02.select_newest(node_id, limit_count)

    # 3. 取得したデータをPandasのデータフレーム（表形式）に変換
    df = pd.DataFrame(result)
    
    # 動作確認のため、取得したデータをコンソールに表示
    print(df)
    
    # DataFrameから対応する行・列の数値を取得
    value1 = df.loc[1, "temperature"]
    value2 = df.loc[1, "humidity"]
    value3 = df.loc[1, "pressure"]
    
    # LEDDisplayの value は文字列を受け取るため、str()で変換して返す
    return str(value1), str(value2), str(value3)

# 5. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(debug=False)