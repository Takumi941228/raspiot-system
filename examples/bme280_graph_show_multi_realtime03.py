# ==========================================
# ライブラリ・モジュールの読み込み (インポート)
# ==========================================
# 自作のデータベース操作用モジュール（DB接続やデータ取得を行う関数がまとめられています）
import db_ambient_count02

# データ処理・分析用ライブラリ（取得したデータを表形式で扱うために使用）
import pandas as pd

# グラフ描画用ライブラリ（直感的に美しいグラフを作成できるPlotly Expressを使用）
import plotly.express as px

# Webアプリケーション作成用ライブラリ (Dash)
# - Dash: アプリの本体
# - dcc (Dash Core Components): グラフ、ドロップダウン、ラジオボタンなどのUI部品
# - html (Dash HTML Components): HTMLタグ（見出しや枠組みなど）を作成する部品
# - callback, Output, Input: ユーザー操作や時間経過に応じて画面を動的に更新する仕組み
from dash import Dash, dcc, html, callback, Output, Input

# ==========================================
# Webアプリの初期化と事前設定
# ==========================================
# Dashアプリケーションのインスタンスを生成
app = Dash()

# 起動時にコンソール（ターミナル）でユーザーに自動更新の間隔を入力させる
print('最新のデータをリアルタイムに表示します。')
print('グラフの更新周期(秒)は？')

# input() で受け取った文字列データを、数値計算ができるように整数型 (int) に変換
update_cycle = int(input('数値を入力(例: 10) : '))

# ==========================================
# 画面レイアウト（UI）の定義
# ==========================================
# app.layout に画面に表示する部品（HTML要素やDashコンポーネント）を配置していきます
app.layout = html.Div([
    # タイトル見出し (<h1> タグに相当)
    html.H1(children=f"Environmental data"),
    
    # 【ラジオボタンUI】データ取得元のノード（機器）を選択
    dcc.RadioItems(
        id='node-select', # コールバックでこの要素の値を参照するためのID
        options=[
            {'label': 'Raspberry Pi Data', 'value':'tochigi_iot_0XX'}, # 表示名: label, 送信する値: value
            {'label': 'ESP32 Data', 'value':'tochigi_mqtt_0XX'}
        ],
        value='tochigi_iot_999' # 初期選択値
    ),
    
    # 【数値入力ボックスUI】表示するデータサンプル数の設定
    html.Div([
        html.Label("何サンプル前のデータまで表示しますか？"), # 説明ラベル
        dcc.Input(
            id='limit-input', # コールバック用のID
            type='number',     # 数値入力専用ボックス
            value=20           # 初期値（最新20件）
        )
    ]),
    
    # 【ドロップダウンUI】表示する環境データ（温度・湿度・気圧）の選択
    dcc.Dropdown(
        id='metric-select', # コールバック用のID
        options=[
            {'label': 'Temperature[deg.C]', 'value':'temperature'}, # 気温
            {'label': 'Humidity[%]', 'value':'humidity'},          # 湿度
            {'label': 'Pressure[hPa]', 'value':'pressure'}         # 気圧
        ],
        value='temperature' # 初期選択値（気温）
    ),
    
    # 【タイマー部品】指定したミリ秒ごとに自動でイベント（n_intervalsのカウントアップ）を発生させる
    dcc.Interval(
        id='interval-component',
        interval=update_cycle * 1000,  # 秒数をミリ秒単位に変換 (例: 10秒 = 10000ミリ秒)
        n_intervals=0                  # カウンターの初期値
    ),
    
    # 【グラフ描画エリア】生成したPlotlyグラフを表示する場所
    dcc.Graph(id='live-graph')
])

# ==========================================
# コールバック処理（自動更新の仕組み）
# ==========================================
# @app.callback デコレータ: 入力(Input)の変化やタイマーの更新を検知して、出力(Output)を自動更新する
@app.callback(
    Output('live-graph', 'figure'),           # 【出力 target】'live-graph' の 'figure' (グラフ画像) を更新
    Input('interval-component', 'n_intervals'),# 【入力 1】タイマーのカウント（定期更新のトリガー）
    Input('node-select', 'value'),            # 【入力 2】選択されたノードID
    Input('limit-input', 'value'),           # 【入力 3】指定された取得サンプル数
    Input('metric-select', 'value')           # 【入力 4】選択された表示項目（気温/湿度/気圧）
)
def update_graph(n, node_id, limit_count, metric):
    """
    入力値が変更されるか、Intervalの時間が来るたびに実行される関数。
    データベースから最新データを取得し、折れ線グラフを再描画して返します。
    """
    # 1. データベースサーバーに接続
    db_ambient_count02.connect()

    # 2. 指定されたノードIDと件数条件で最新データをクエリ（検索実行）
    result = db_ambient_count02.select_newest(node_id, limit_count)

    # 3. 取得したデータをPandasのデータフレーム（表形式）に変換
    df = pd.DataFrame(result)
 
    # 動作確認のため、取得したデータをコンソールに表示
    print(df)

    # 4. 選択された項目（metric）に応じてグラフを生成
    if metric == 'temperature':
        # --- 気温のグラフ（赤色） ---
        fig = px.line(
            df,
            x='timestamp',   # X軸: 日時
            y='temperature', # Y軸: 気温
            title=f'Temperature Trend(Node: {node_id}, Every {update_cycle} sec. cycle)',
            labels={'timestamp': 'TimeStamp', 'temperature': 'Temperature [deg.C]'},
            color_discrete_sequence=['red']  # 折れ線の色を「赤」に設定
        )
    elif metric == 'humidity':
        # --- 湿度のグラフ（青色） ---
        fig = px.line(
            df,
            x='timestamp', # X軸: 日時
            y='humidity',  # Y軸: 湿度
            title=f'Humidity Trend(Node: {node_id}, Every {update_cycle} sec. cycle)',
            labels={'timestamp': 'TimeStamp', 'humidity': 'Humidity [%]'},
            color_discrete_sequence=['blue']  # 折れ線の色を「青」に設定
        )
    else:
        # --- 気圧のグラフ（緑色） ---
        fig = px.line(
            df,
            x='timestamp', # X軸: 日時
            y='pressure',  # Y軸: 気圧
            title=f'Pressure Trend(Node: {node_id}, Every {update_cycle} sec. cycle)',
            labels={'timestamp': 'TimeStamp', 'pressure': 'Presuure [hPa]'},
            color_discrete_sequence=['green']  # 折れ線の色を「緑」に設定
        )
    
    # 5. X軸のタイムスタンプラベルが見やすいように90度回転させる
    fig.update_xaxes(tickangle=90)

    # 生成したグラフオブジェクトを返し、画面上の 'live-graph' に反映させる
    return fig

# このファイルが直接実行された場合にWebサーバーを起動する
if __name__ == '__main__':
    # Webサーバーの起動（debug=False で本番モード起動）
    app.run(debug=False)
