# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashとラジオボタンUI部品（dcc.RadioItems）を使用して、
# 複数のセンサノード（Raspberry Pi と ESP32）のうち表示したいノードを
# 排他的に選択し、その最新温度データの推移を赤色の折れ線グラフとして
# インタラクティブに可視化するWebアプリケーションです。
# ラジオボタンの選択肢を変更するとコールバックが発火し、自動的にグラフが更新されます。
# ==============================================================================

# 1. ライブラリ・モジュールの読み込み (インポート)
# DB関連をまとめたモジュール（自作モジュール：DBへの接続やデータ取得関数を管理）
import db_ambient_count02

# グラフ表示に関するライブラリ（データフレームという表形式でデータを扱うためのPandas）
import pandas as pd

# グラフ描画用ライブラリ（直感的な操作で高度なグラフを描画できるPlotly Express）
import plotly.express as px

# Webアプリケーション作成用ライブラリ (Dash)
# - Dash: アプリケーション本体
# - dcc (Dash Core Components): ラジオボタンやグラフなどのUI部品
# - html (Dash HTML Components): HTMLタグ（枠組みなど）を作成する部品
# - Output, Input: ユーザ操作に応じて画面を動的に更新するための仕組み
from dash import Dash, dcc, html, callback, Output, Input

# 2. アプリの初期化と起動時パラメータの設定
# アプリの初期化
app = Dash()

# クエリのパラメータをターミナルから事前に入力
print('最新のデータを表示します。')
print('何サンプル前のデータまで表示しますか？')
# 入力したデータを数値（整数）に変換
limit_count = int(input('数値を入力 (例: 10) : '))

# 3. ダッシュボードのレイアウト定義 (UI設計)
# 画面上にラジオボタン（ノード選択用）とグラフ描画エリアを配置します
app.layout = html.Div([
    # 【ラジオボタン】表示したいノードを排他的に選択するためのUI部品
    dcc.RadioItems(
        id='callback-input',  # コールバックで紐付けるためのID
        options=[
            {"label": "Raspberry Pi BME280", "value": "tochigi_iot_0XX"},
            {"label": "ESP32-DevKit-VE BME280", "value": "tochigi_mqtt_0XX"},
        ],
        value="tochigi_iot_0XX"  # 初期選択値
    ),
    
    # 【グラフ描画エリア】生成したPlotlyグラフを表示する場所
    dcc.Graph(id='live-graph')
])

# 4. コールバック処理（ラジオボタン選択に応じたグラフの更新）
# ラジオボタンの選択値が変わった（Inputの変化）のを検知して実行されます。
@app.callback(
    Output('live-graph', 'figure'),         # 【出力】'live-graph' の 'figure' (グラフ画像) を更新
    Input('callback-input', 'value')          # 【入力】選択されたノードのID（value）
)

def update_graph(node_id):
    """
    ラジオボタンで選択されたノードIDを受け取り、DBから最新データを取得して
    対応する気温の折れ線グラフを生成して返す関数
    """
    # 1. データベースサーバに接続
    db_ambient_count02.connect()

    # 2. 指定されたノードIDと件数条件で最新データをクエリ（検索実行）
    result = db_ambient_count02.select_newest(node_id, limit_count)

    # 3. 取得したデータを表形式（Pandas DataFrame）に変換
    df = pd.DataFrame(result)
 
    # 動作確認のため、取得したデータをコンソールに表示
    print(df)

    # 4. Plotly Expressを使った折れ線グラフの生成（赤色）
    fig = px.line(
        df,
        x='timestamp',   # X軸: 日時
        y='temperature', # Y軸: 気温
        title=f'Temperature Trend (Node: {node_id})',
        labels={'timestamp': 'TimeStamp', 'temperature': 'Temperature [deg.C]'},
        color_discrete_sequence=['red']  # 折れ線の色を赤に設定
    )

    # 生成したグラフオブジェクトを返し、画面上の 'live-graph' に反映させる
    return fig

# 5. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8050, debug=False)