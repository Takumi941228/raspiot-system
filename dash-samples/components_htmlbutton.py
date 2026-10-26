# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashとHTMLボタン（html.Button）、および callback_context を
# 使用して、ユーザが画面上のどのボタン（Temp / Humi / Press）を押したかを検知し、
# 対応するセンサー指標の折れ線グラフを動的に切り替えて表示する
# Webアプリケーションです。
# ボタンがクリックされるたびにコールバックが発火し、データベースから最新データを
# 取得して指定されたカラーのグラフに再描画します。
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
# - dcc (Dash Core Components): グラフ描画エリアなどのUI部品
# - html (Dash HTML Components): HTMLタグ（見出しやボタン、枠組みなど）を作成する部品
# - Output, Input: ユーザ操作に応じて画面を動的に更新するための仕組み
# - callback_context: 複数ある入力のうち、どれがトリガ（操作）されたかを判別する仕組み
from dash import Dash, dcc, html, Output, Input, callback_context

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
# タイトル見出し、切り替え用の3つのボタン、グラフ表示エリアを配置します
app.layout = html.Div([
    # 【タイトルエリア】
    html.Div([
        html.H1("PUSH BUTTON"),
        html.H2("Change Graph"),
    ], style={"color": "red", "textAlign": "center", "fontSize": 30}),
    
    # 【操作ボタンエリア】
    html.Button(id="b-one", children="Temp", style={"height": 50, "width": 100, "borderRadius": "50%", "fontSize": 25, "margin": "5px"}),
    html.Button(id="b-two", children="Humi", style={"height": 50, "width": 100, "borderRadius": "50%", "fontSize": 25, "margin": "5px"}),
    html.Button(id="b-three", children="Press", style={"height": 50, "width": 100, "borderRadius": "50%", "fontSize": 25, "margin": "5px"}),
    
    # 【グラフ描画エリア】生成したPlotlyグラフを表示する場所
    html.Div([
        dcc.Graph(id='live-graph')
    ])
])


# 4. コールバック処理（ボタン操作に応じたグラフの切り替え）
# 3つのボタンのいずれかが押された（n_clicksの変化）のを検知して実行されます。
@app.callback(
    Output('live-graph', 'figure'),         # 【出力】'live-graph' の 'figure' (グラフ画像) を更新
    Input('b-one', 'n_clicks'),             # 【入力】ボタン1（Temp）のクリック検知
    Input('b-two', 'n_clicks'),             # 【入力】ボタン2（Humi）のクリック検知
    Input('b-three', 'n_clicks'),           # 【入力】ボタン3（Press）のクリック検知
)

def update_graph(c_one, c_two, c_three):
    """
    どのボタンが押されたかを判定し、対応する指標（気温・湿度・気圧）の折れ線グラフを生成して返す関数
    """
    # 1. データベースサーバに接続
    db_ambient_count02.connect()

    # 2. 指定されたノードIDと件数条件で最新データをクエリ（検索実行）
    result = db_ambient_count02.select_newest(node_id, limit_count)

    # 3. 取得したデータを表形式（Pandas DataFrame）に変換
    df = pd.DataFrame(result)
 
    # 動作確認のため、取得したデータをコンソールに表示
    print(df)

    # 4. callback_context を使って、今回どのコンポーネントが操作（トリガ）されたかを特定
    select_id = callback_context.triggered[0]["prop_id"].split(".")[0]

    # 5. 押されたボタンに応じてグラフのデザインや軸を切り替え
    if select_id == 'b-one':
        # --- 気温のグラフ（赤色） ---
        fig = px.line(
            df,
            x='timestamp',   # X軸: 日時
            y='temperature', # Y軸: 気温
            title=f'Temperature Trend (Node: {node_id})',
            labels={'timestamp': 'TimeStamp', 'temperature': 'Temperature [deg.C]'},
            color_discrete_sequence=['red']  # 折れ線の色を赤に設定
        )
    elif select_id == 'b-two':
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
        # --- 気圧のグラフ（緑色 / 初期表示もここに含まれます） ---
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
    app.run(debug=False)