# ライブラリ・モジュールの読み込み (インポート)
# DB関連をまとめたモジュール（自作モジュール：データベース接続やデータ取得を行う）
import db_ambient_count02

# グラフ表示に関するライブラリ（取得データを表形式で扱うPandas）
import pandas as pd

# グラフ描画用ライブラリ（直感的にインタラクティブなグラフを作成できるPlotly Express）
import plotly.express as px

# Webアプリに関するライブラリ（Dash）
# - Dash: アプリケーション本体を作成
# - dcc (Dash Core Components): グラフ描画エリアや自動更新タイマーなどのUI部品
# - html (Dash HTML Components): HTMLの見た目（見出しや枠組み）を作る部品
# - callback, Output, Input: イベント（タイマーなど）を検知して画面を自動更新する仕組み
from dash import Dash, dcc, html, callback, Output, Input

# アプリの初期化とパラメーターの入力設定
# アプリの初期化（Dashのインスタンス生成）
app = Dash()

# クエリのパラメータを入力
# 表示を開始する日付・時刻を入力する（コンソールに対話形式の案内を表示）
print('最新のデータをリアルタイムに表示します。')
print('どのノードのデータを表示しますか？')

# input() で入力された文字列を対象のノードIDとして取得
node_id = input('ノードの Identifier(例: tochigi_iot_0XX): ')

print('何サンプル前のデータまで表示しますか？')
# 入力したデータを数値に変換（文字列から整数型 int へ変換）
limit_count = int(input('数値を入力(例: 20) : '))

print('グラフの更新周期(秒)は？')
# 入力したデータを数値に変換（更新秒数を整数型 int へ変換）
update_cycle = int(input('数値を入力(例: 10) : '))

# ダッシュボードレイアウトの定義
# ダッシュボードレイアウトの変更（画面上に配置する要素の組み立て）
app.layout = html.Div([
    # タイトル見出し (<h1> タグに相当)
    html.H1(children=f"Environmental data"),
    
    # 自動更新タイマー（指定した秒数ごとにイベントを発生させる部品）
    dcc.Interval(
        id='interval-component',
        interval=update_cycle * 1000,  # 秒数をミリ秒に変換 (例: 10秒 = 10000ミリ秒)
        n_intervals=0                  # タイマーのカウント初期値
    ),
    
    # 3つのグラフ描画エリアを縦に配置
    dcc.Graph(id='live-graph1'), # 気温用グラフを表示するエリア
    dcc.Graph(id='live-graph2'), # 湿度用グラフを表示するエリア
    dcc.Graph(id='live-graph3')  # 気圧用グラフを表示するエリア
])

# 自動更新のコールバック処理とグラフ自動描画
# 自動更新のコールバック内容
# タイマー(interval-component)がカウントアップするたびに update_graph 関数を実行
@app.callback(
    Output('live-graph1', 'figure'), # 【出力 1】1つ目のグラフ(気温)の描画データ
    Output('live-graph2', 'figure'), # 【出力 2】2つ目のグラフ(湿度)の描画データ
    Output('live-graph3', 'figure'), # 【出力 3】3つ目のグラフ(気圧)の描画データ
    Input('interval-component', 'n_intervals') # 【入力】タイマーの経過カウント（定期実行のトリガー）
)

# 更新周期毎にグラフの自動描画を行う関数
def update_graph(n):
    # DBサーバに接続する
    db_ambient_count02.connect()

    # クエリを実施して結果を得る（選択ノード・件数指定で最新データを取得）
    result = db_ambient_count02.select_newest(node_id, limit_count)

    # 結果を表形式（Pandas DataFrame）に変換する
    df = pd.DataFrame(result)
 
    # コンソール表示（取得したデータをターミナルで確認）
    print(df)

    # 1. 気温グラフの生成
    fig1 = px.line(
        df,
        x='timestamp',   # X軸: 日時
        y='temperature', # Y軸: 気温
        title=f'Temperature Trend(Node: {node_id}, Every {update_cycle} sec. cycle)',
        labels={'timestamp': 'TimeStamp', 'temperature': 'Temperature [deg.C]'},
        color_discrete_sequence=['red']  # 折れ線の色を「赤」に設定
    )
    fig1.update_xaxes(tickangle=90)  # x軸ラベルを90度回転（重なり防止）

    # 2. 湿度グラフの生成
    fig2 = px.line(
        df,
        x='timestamp', # X軸: 日時
        y='humidity',  # Y軸: 湿度
        title=f'Humidity Trend(Node: {node_id}, Every {update_cycle} sec. cycle)',
        labels={'timestamp': 'TimeStamp', 'humidity': 'Humidity [%]'},
        color_discrete_sequence=['blue']  # 折れ線の色を「青」に設定
    )
    fig2.update_xaxes(tickangle=90)  # x軸ラベルを90度回転

    # 3. 気圧グラフの生成
    fig3 = px.line(
        df,
        x='timestamp', # X軸: 日時
        y='pressure',  # Y軸: 気圧
        title=f'Pressure Trend(Node: {node_id}, Every {update_cycle} sec. cycle)',
        labels={'timestamp': 'TimeStamp', 'pressure': 'Presuure [hPa]'},
        color_discrete_sequence=['green']  # 折れ線の色を「緑」に設定
    )
    fig3.update_xaxes(tickangle=90)  # x軸ラベルを90度回転

    # 生成した3つのグラフオブジェクトを順番に返す（コールバックのOutput順に対応）
    return fig1, fig2, fig3

# アプリケーションの実行
# Run the app（スクリプトが直接実行された場合にのみWebサーバーを起動）
if __name__ == '__main__':
    app.run(debug=False)
