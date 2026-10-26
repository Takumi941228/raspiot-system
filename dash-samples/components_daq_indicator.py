# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashとDash DAQのインジケータ（daq.Indicator）を使用して、
# 指定したセンサーノードの温度データを定期的に取得し、閾値（28.0°C）を超える高温状態に
# なった場合にランプを点灯させて視覚的に警告するリアルタイム監視Webアプリケーションです。
# 5秒ごとに自動更新され、現在の温度状態をインジケータとラベルに動的に反映します。
# ==============================================================================

# 1. ライブラリ・モジュールの読み込み (インポート)
# DB関連をまとめたモジュール（自作モジュール：DBへの接続やデータ取得関数を管理）
import db_ambient_count02

# グラフ表示に関するライブラリ（データフレームという表形式でデータを扱うためのPandas）
import pandas as pd

# Dashでインジケータ（状態表示ランプ）などの高度なUI部品を使うためのライブラリ
import dash_daq as daq

# Webアプリケーション作成用ライブラリ (Dash)
# - Dash: アプリケーション本体
# - dcc (Dash Core Components): タイマ（Interval）などのUI部品
# - html (Dash HTML Components): HTMLタグ（枠組みなど）を作成する部品
# - Output, Input: 画面を動的に更新するための仕組み
from dash import Dash, dcc, html, Output, Input

# 2. アプリの初期化と起動時パラメタの設定
# アプリの初期化
app = Dash()

# クエリのパラメータをターミナルから事前に入力
print('最新のセンサーデータを監視します。')
print('どのノードのデータを監視しますか？')
node_id = input('ノードの Identifier (例: tochigi_mqtt_0XX): ')

print('何サンプル前のデータまで参照しますか？')
# 入力したデータを数値（整数）に変換
limit_count = int(input('数値を入力 (例: 10) : '))

# 3. ダッシュボードのレイアウト定義 (UI設計)
# 画面上に状態を示すIndicator（インジケーター）と、自動更新用のタイマを配置します
app.layout = html.Div([
    # 【自動更新タイマ】指定したミリ秒ごとにコールバックを呼び出す（例: 5000ms = 5秒ごと）
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # 更新間隔（ミリ秒）
        n_intervals=0       # 起動からの経過カウント
    ),
    
    # 【インジケータ部品】温度の状態（警告ランプなど）を視覚的に表示
    html.H2(f"Node Status : {node_id}"),
    daq.Indicator(
        id='our-indicator',
        label="Temperature Warning (> 28.0°C)",
        value=False        # 初期状態（False: 消灯 / True: 点灯）
    ),
])

# 4. コールバック処理（定期的なデータ取得とインジケータの更新）
# タイマ（dcc.Interval）が一定時間ごとに進む（Inputの変化）のを検知して実行されます。
@app.callback(
    Output('our-indicator', 'value'),
    Output('our-indicator', 'label'),
    Input('interval-component', 'n_intervals')  # タイマのカウント変化をトリガーにする
)

def update_indicator(n_intervals):
    """
    タイマの時間が来るたびに実行される関数。
    データベースから最新データを取得し、温度の条件に応じてインジケータの点灯/消灯を切り替えます。
    """
    # 1. データベースサーバに接続
    db_ambient_count02.connect()

    # 2. 指定されたノードIDと件数条件で最新データをクエリ（検索実行）
    result = db_ambient_count02.select_newest(node_id, limit_count)

    # 3. 取得したデータをPandasのデータフレーム（表形式）に変換
    df = pd.DataFrame(result)
    
    # 動作確認のため、取得したデータをコンソールに表示
    print(df)
    
    # DataFrameから最新の温度データを取得
    current_temp = df.loc[1, "temperature"]
    
    # 4. 温度が28.0度を超えているかでインジケータの点灯状態（True/False）を判定
    is_hot = bool(current_temp > 28.0)
    
    # インジケータのラベルに現在の温度を動的に反映
    status_label = f"Current Temp: {current_temp}°C (Threshold: 28.0°C)"
    
    # インジケータの状態（点灯フラグ）と新しいラベルを返す
    return is_hot, status_label

# 5. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(debug=False)