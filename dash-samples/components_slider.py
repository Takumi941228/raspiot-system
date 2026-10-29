# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashとスライダUI部品（dcc.Slider）を使用して、
# ユーザがWebブラウザ上でスライダを操作しながらグラフに表示するサンプル数
# （データ件数: 2〜1000件）を動的に変更できるWebアプリケーションです。
# スライダの値変更（ドラッグ中含む）を検知してコールバックが発火し、
# データベースから指定された件数の最新データを取得して赤色の折れ線グラフを
# リアルタイムに再描画します。
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
# - dcc (Dash Core Components): スライダやグラフなどのUI部品
# - html (Dash HTML Components): HTMLタグ（枠組みなど）を作成する部品
# - Output, Input: ユーザ操作に応じて画面を動的に更新するための仕組み
from dash import Dash, dcc, html, callback, Output, Input

# 2. アプリの初期化と起動時パラメータの設定
# アプリの初期化
app = Dash()

# クエリのパラメータをターミナルから事前に入力
print('最新のデータを表示します。')
print('どのノードのデータを表示しますか？')
node_id = input('ノードの Identifier (例: tochigi_mqtt_0XX): ')

# 3. ダッシュボードのレイアウト定義 (UI設計)
# 画面上に値変更用のスライダとグラフ描画エリアを配置します
app.layout = html.Div([
    # 【スライダ部品】取得するサンプル数（件数）を動的に変更するためのUI
    html.P("折れ線グラフのサンプル数"),
    dcc.Slider(
        id='callback-input',  # コールバックで紐付けるためのID
        min=2,                # 最小値
        max=1000,             # 最大値
        value=10,             # 初期値
        updatemode="drag",    # ドラッグ中にリアルタイムでコールバックをトリガする設定
        marks={2: '2', 250: '250', 500: '500', 750: '750', 1000: '1000'}  # 目盛り
    ),
    
    # 【グラフ描画エリア】生成したPlotlyグラフを表示する場所
    dcc.Graph(id='live-graph')
])

# 4. コールバック処理（スライダ操作に応じたグラフの更新）
# スライダの値が変わった（Inputの変化）のを検知して実行されます。
@app.callback(
    Output('live-graph', 'figure'),         # 【出力】'live-graph' の 'figure' (グラフ画像) を更新
    Input('callback-input', 'value')          # 【入力】スライダで選択された数値（サンプル数 / limit_count）
)

def update_graph(limit_count):
    """
    スライダから渡されたサンプル数を受け取り、DBから最新データを取得して
    対応する気温の折れ線グラフを生成して返す関数
    """
    # 1. データベースサーバに接続
    db_ambient_count02.connect()

    # 2. 指定されたノードIDと件数条件で最新データをクエリ（検索実行）
    result = db_ambient_count02.select_newest(node_id, limit_count)

    # 3. 取得したデータを表形式（Pandas DataFrame）に変換
    df = pd.DataFrame(result)
 
    # 動作確認のため、取得したデータをコンソールに表示
    print(f"取得サンプル数: {limit_count}")
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