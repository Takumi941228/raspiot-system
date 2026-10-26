# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashとDash DAQのゲージ（Gauge）コンポーネント、および
# 自動更新タイマ（dcc.Interval）を使用して、指定したセンサノードの
# 温度・湿度・気圧の最新データをリアルタイム（5秒ごと）に取得・表示する
# ダッシュボードWebアプリケーションです。
# ユーザーは起動時にターミナルから対象ノードIDとサンプル数を入力します。
# ==============================================================================

# 1. ライブラリ・モジュールの読み込み (インポート)
# DB関連をまとめたモジュール（自作モジュール：DBへの接続やデータ取得関数を管理）
import db_ambient_count02

# グラフ表示に関するライブラリ（データフレームという表形式でデータを扱うためのPandas）
import pandas as pd

# Dashでデジタルメーターやゲージなどの高度なUI部品を使うためのライブラリ
import dash_daq as daq

# Webアプリケーション作成用ライブラリ (Dash)
# - Dash: アプリケーション本体
# - dcc (Dash Core Components): タイマ（Interval）などのUI部品
# - html (Dash HTML Components): HTMLタグ（枠組みなど）を作成する部品
# - Output, Input: 画面を動的に更新するための仕組み
from dash import Dash, dcc, html, Output, Input

# 2. アプリの初期化と起動時パラメータの設定
# アプリのインスタンス生成
app = Dash()

# クエリのパラメータをターミナルから入力
print('最新のデータを表示します。')
print('どのノードのデータを表示しますか？')
node_id = input('ノードの Identifier (例: tochigi_mqtt_0XX): ')

print('何サンプル前のデータまで表示しますか？')
# 入力したデータを数値（整数）に変換
limit_count = int(input('数値を入力 (例: 10) : '))

# 3. ダッシュボードのレイアウト定義 (UI設計)
# 画面上に3つのゲージ（温度・湿度・気圧）と、自動更新用のタイマを配置します
app.layout = html.Div([
    # 【自動更新タイマー】指定したミリ秒ごとにコールバックを呼び出す（例: 5000ms = 5秒ごと）
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # 更新間隔（ミリ秒）
        n_intervals=0       # 起動からの経過カウント
    ),
    
    # 【ゲージ部品】温度、湿度、気圧を表示するメータ
    daq.Gauge(
        id='our-gauge1',
        label="Temp [°C]",
        min=0.0,
        max=40.0,
        value=0,
        showCurrentValue=True,
        units="deg.C"
    ),
    daq.Gauge(
        id='our-gauge2',
        label="Humi [%]",
        min=0.0,
        max=100.0,
        value=0,
        showCurrentValue=True,
        units="%",
    ),
    daq.Gauge(
        id='our-gauge3',
        label="Press [hPa]",
        min=800.0,
        max=1100.0,
        value=0,
        showCurrentValue=True,
        units="hPa",
    ),
], style={'textAlign': 'center'})

# 4. コールバック処理（定期的なデータ取得とゲージの更新）
# タイマ（dcc.Interval）が一定時間ごとに進む（Inputの変化）のを検知して実行されます。
@app.callback(
    Output('our-gauge1', 'value'),
    Output('our-gauge2', 'value'),
    Output('our-gauge3', 'value'),
    Input('interval-component', 'n_intervals')  # タイマーのカウント変化をトリガーにする
)

def update_output(n_intervals):
    """
    タイマーの時間が来るたびに実行される関数。
    データベースから最新データを取得し、各ゲージの値を更新して返します。
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
    # ※ 特定の行（例: インデックス1）のデータを抽出してゲージに反映
    value1 = df.loc[1, "temperature"]
    value2 = df.loc[1, "humidity"]
    value3 = df.loc[1, "pressure"]
    
    # 各ゲージの value に対応する値を順番に返す
    return value1, value2, value3

# 5. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(debug=False)