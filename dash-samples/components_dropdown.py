# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashとドロップダウンUI部品（dcc.Dropdown）を使用して、
# 指定したセンサノードの最新データから「温度」「湿度」「気圧」のいずれかを選択し、
# 項目に応じたカラー（赤・青・緑）の折れ線グラフとしてインタラクティブに可視化する
# Webアプリケーションです。
# ドロップダウンで指標を切り替えるとコールバックが発火し、自動的にグラフが更新されます。
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
# - dcc (Dash Core Components): ドロップダウンやグラフなどのUI部品
# - html (Dash HTML Components): HTMLタグ（枠組みなど）を作成する部品
# - Output, Input: ユーザ操作に応じて画面を動的に更新するための仕組み
from dash import Dash, dcc, html, Output, Input

# 2. アプリの初期化と起動時パラメータの設定
# アプリの初期化
app = Dash()

# クエリのパラメータをターミナルから事前に入力
print('最新のデータを表示します。')
print('どのノードのデータを表示しますか？')
node_id = input('ノードの Identifier (例: tochigi_mqtt_0XX): ')

print('何サンプル前のデータまで表示しますか？')
# 入力したデータを数値（整数）に変換
limit_count = int(input('数値を入力 (例: 10) : '))

# 3. ダッシュボードのレイアウト定義 (UI設計)
# 画面上にドロップダウンメニューとグラフ描画エリアを配置します
app.layout = html.Div([
    # 【ドロップダウン】表示する指標（気温/湿度/気圧）を選択するためのUI部品
    dcc.Dropdown(
        id='metric-select',  # コールバックで紐付けるためのID
        options=[
            {"label": "Temperature", "value": "temperature"},
            {"label": "Humidity", "value": "humidity"},
            {"label": "Pressure", "value": "pressure"},
        ],
        value="temperature",  # 初期選択値
        clearable=False      # 選択をクリアできないようにする設定
    ),
    
    # 【グラフ描画エリア】生成したPlotlyグラフを表示する場所
    dcc.Graph(id='live-graph')
])

# 4. コールバック処理（ドロップダウン選択に応じたグラフの更新）
# ドロップダウンの選択値が変わった（Inputの変化）のを検知して実行されます。
@app.callback(
    Output('live-graph', 'figure'),         # 【出力】'live-graph' の 'figure' (グラフ画像) を更新
    Input('metric-select', 'value')         # 【入力】選択された表示項目（temperature / humidity / pressure）
)
def update_graph(metric):
    """
    ドロップダウンで選択された指標を受け取り、DBから最新データを取得して
    対応する色・タイトルの折れ線グラフを生成して返す関数
    """
    # 1. データベースサーバに接続
    db_ambient_count02.connect()

    # 2. 指定されたノードIDと件数条件で最新データをクエリ（検索実行）
    result = db_ambient_count02.select_newest(node_id, limit_count)

    # 3. 取得したデータを表形式（Pandas DataFrame）に変換
    df = pd.DataFrame(result)
 
    # 動作確認のため、取得したデータをコンソールに表示
    print(df)

    # 4. 選択された項目（metric）に応じてグラフのデザインや軸を切り替え
    if metric == 'temperature':
        # --- 気温のグラフ（赤色） ---
        fig = px.line(
            df,
            x='timestamp',   # X軸: 日時
            y='temperature', # Y軸: 気温
            title=f'Temperature Trend (Node: {node_id})',
            labels={'timestamp': 'TimeStamp', 'temperature': 'Temperature [deg.C]'},
            color_discrete_sequence=['red']  # 折れ線の色を赤に設定
        )
    elif metric == 'humidity':
        # --- 湿度のグラフ（青色） ---
        fig = px.line(
            df,
            x='timestamp',   # X軸: 日時
            y='humidity',    # Y軸: 湿度
            title=f'Humidity Trend (Node: {node_id})',
            labels={'timestamp': 'TimeStamp', 'humidity': 'Humidity [%]'},
            color_discrete_sequence=['blue']  # 折れ線の色を青に設定
        )
    else:
        # --- 気圧のグラフ（緑色） ---
        fig = px.line(
            df,
            x='timestamp',   # X軸: 日時
            y='pressure',    # Y軸: 気圧
            title=f'Pressure Trend (Node: {node_id})',
            labels={'timestamp': 'TimeStamp', 'pressure': 'Pressure [hPa]'},  
            color_discrete_sequence=['green']  # 折れ線の色を緑に設定
        )
    
    # 生成したグラフオブジェクトを返し、画面上の 'live-graph' に反映させる
    return fig

# 5. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8050, debug=False)