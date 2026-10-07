# ライブラリ・モジュールの読み込み (インポート)
# DB関連をまとめたモジュール（自作モジュール：DBへの接続やデータ取得関数を管理）
import db_ambient_count02

# グラフ表示に関するライブラリ（データフレームという表形式でデータを扱うためのPandas）
import pandas as pd

# グラフ描画用ライブラリ（直感的な操作で高度なグラフを描画できるPlotly Express）
import plotly.express as px

# Webアプリに関するライブラリ（Dash）
# - Dash: Webアプリケーション本体を作成するクラス
# - dcc (Dash Core Components): ドロップダウンやタイマーなどのUI部品
# - html (Dash HTML Components): HTMLタグ（見出しや枠組みなど）を作成する部品
# - callback, Output, Input: ユーザー操作や時間の変化に応じて表示を自動更新する仕組み
from dash import Dash, dcc, html, callback, Output, Input

# アプリの初期化と入力設定（コンソール対話）
# アプリの初期化（Dashアプリケーションのインスタンスを生成）
app = Dash()

# クエリのパラメータを入力
# 表示を開始する日付・時刻を入力する（コンソールに案内を表示）
print('最新のデータをリアルタイムに表示します。')
print('どのノードのデータを表示しますか？')

# input() でキーボードからの入力文字列を受け取り、対象ノードIDとして変数に代入
node_id = input('ノードの Identifier(例: tochigi_iot_0XX): ')

print('何サンプル前のデータまで表示しますか？')
# 入力したデータを数値に変換（input() の戻り値は文字列のため int() で整数に変換）
limit_count = int(input('数値を入力(例: 20) : '))

print('グラフの更新周期(秒)は？')
# 入力したデータを数値に変換（同じく整数型に変換して自動更新の間隔を設定）
update_cycle = int(input('数値を入力(例: 10) : '))

# ダッシュボードレイアウトの定義
# ダッシュボードレイアウトの変更（画面に配置する見た目のコンポーネントを定義）
app.layout = html.Div([
    # タイトル見出し (<h1> タグ)
    html.H1(children=f"Environmental data"),
    
    # ドロップダウンボックスの追加（表示する項目を選択するUI）
    dcc.Dropdown(
        id='metric-select', # コールバック関数で参照するためのID
        options=[
            {'label': 'Temperature[deg.C]', 'value':'temperature'}, # 表示名: label, 値: value
            {'label': 'Humidity[%]', 'value':'humidity'},
            {'label': 'Pressure[hPa]', 'value':'pressure'}
        ],
        value='temperature' # 初期値をtemperature（気温）に設定
    ),
    
    # 自動更新タイマーコンポーネント（一定時間ごとにイベントを発火させる）
    dcc.Interval(
        id='interval-component', # コールバック用のID
        interval=update_cycle * 1000,  # 秒数をミリ秒単位に変換（例: 10秒 = 10000ミリ秒）
        n_intervals=0                  # カウントの初期値
    ),
    
    # グラフ描画エリア（生成したPlotlyのグラフが表示される領域）
    dcc.Graph(id='live-graph')
])

# 自動更新のコールバック定義とグラフ描画関数
# 自動更新のコールバック内容
# Input の値が変更されるか、Intervalの時間が来るたびに update_graph 関数が自動実行される
@app.callback(
    Output('live-graph', 'figure'),            # 【出力】id='live-graph' の 'figure'(グラフデータ) に結果を返す
    Input('interval-component', 'n_intervals'),# 【入力1】タイマーの経過カウント（定期実行のトリガー）
    Input('metric-select', 'value')            # 【入力2】ドロップダウンで選択された項目（temperature/humidity/pressure）
)

# 更新周期毎にグラフの自動描画を行う関数
def update_graph(n, metric):
    # DBサーバに接続する
    db_ambient_count02.connect()

    # クエリを実施して結果を得る（選択されたノードと指定サンプル数で検索）
    result = db_ambient_count02.select_newest(node_id, limit_count)

    # 結果を表形式（Pandas DataFrame）に変換する
    df = pd.DataFrame(result)
 
    # コンソール表示（取得したデータをターミナルで確認用に出力）
    print(df)

    # 引数metricの値によって描画するグラフを決定
    if metric == 'temperature':
        # グラフ生成（気温用）
        fig = px.line(
            df,
            x='timestamp',   # X軸: 日時
            y='temperature', # Y軸: 気温
            title=f'Temperature Trend(Node: {node_id}, Every {update_cycle} sec. cycle)',
            labels={'timestamp': 'TimeStamp', 'temperature': 'Temperature [deg.C]'},
            color_discrete_sequence=['red']  # 赤に変更
        )
    elif metric == 'humidity':
        # グラフ生成（湿度用）
        fig = px.line(
            df,
            x='timestamp', # X軸: 日時
            y='humidity',  # Y軸: 湿度
            title=f'
