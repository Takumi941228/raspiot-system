# ライブラリ・モジュールの読み込み (インポート)
# DB関連をまとめたモジュール（自作モジュール：データベース接続や最新データの検索を行う関数を定義）
import db_ambient_count02

# グラフ表示に関するライブラリ（取得したデータを表形式で効率的に扱うためのPandas）
import pandas as pd

# グラフ描画用ライブラリ（直感的な記述で折れ線グラフなどを描画できるPlotly Express）
import plotly.express as px

# Webアプリに関するライブラリ（Dash）
# - Dash: Webアプリケーション本体を生成
# - dcc (Dash Core Components): グラフ領域や定期更新用タイマーなどのUI部品
# - html (Dash HTML Components): HTMLのタグ構造（見出しやレイアウト枠組み）を作る部品
# - callback, Output, Input: 画面要素の変化やタイマーを検知して表示を更新する仕組み
from dash import Dash, dcc, html, callback, Output, Input

# アプリの初期化と入力設定（コンソール対話）
# アプリの初期化（Dashアプリケーションのインスタンス作成）
app = Dash()

# クエリのパラメータを入力
# 表示を開始する日付・時刻を入力する（コンソールに案内を表示）
print('最新の気温データをリアルタイムに表示します。')
print('どのノードのデータを表示しますか？')

# input() で入力された文字列を受け取り、対象となるノードIDとして変数に格納
node_id = input('ノードの Identifier(例: tochigi_iot_0XX): ')

print('何サンプル前のデータまで表示しますか？')
# 入力したデータを数値に変換（input()の戻り値は文字列のため int() で整数化）
limit_count = int(input('数値を入力(例: 20) : '))

print('グラフの更新周期(秒)は？')
# 入力したデータを数値に変換（自動更新間隔となる秒数を整数化）
update_cycle = int(input('数値を入力(例: 10) : '))

# ダッシュボードレイアウトの定義
# ダッシュボードレイアウトの変更（Web画面の見た目・配置を設定）
app.layout = html.Div([
    # タイトル見出し (<h1> タグ: 選択されたノードIDを表示)
    html.H1(children=f"Temperature Trend (Node: {node_id})"),
    
    # 自動更新タイマー（指定された周期ごとにイベントを発火させるコンポーネント）
    dcc.Interval(
        id='interval-component',
        interval=update_cycle * 1000,  # 秒数をミリ秒単位に変換（例: 10秒 = 10000ミリ秒）
        n_intervals=0                  # カウントの初期値
    ),
    
    # グラフ描画エリア（生成された気温グラフが表示される領域）
    dcc.Graph(id='live-graph')
])

# 自動更新のコールバック定義とグラフ自動描画
# 自動更新のコールバック内容
# タイマー(interval-component)が更新されるたびに update_graph 関数を自動呼び出し
@app.callback(
    Output('live-graph', 'figure'),            # 【出力】id='live-graph' の 'figure'(グラフ画像データ) に反映
    Input('interval-component', 'n_intervals') # 【入力】タイマーの経過カウント（自動実行のトリガー）
)

# 更新周期毎にグラフの自動描画を行う関数
def update_graph(n):
    # DBサーバに接続する
    db_ambient_count02.connect()

    # クエリを実施して結果を得る（選択されたノードと件数指定で最新データを取得）
    result = db_ambient_count02.select_newest(node_id, limit_count)

    # 結果を表形式（Pandas DataFrame）に変換する
    df = pd.DataFrame(result)
 
    # コンソール表示（取得したデータの内容をターミナルで確認）
    print(df)

    # グラフ生成（気温データの折れ線グラフを作成）
    fig = px.line(
        df,
        x='timestamp',   # X軸: 日時データ
        y='temperature', # Y軸: 気温データ
        title=f'Temperature Trend(Node: {node_id}, Every {update_cycle} sec. cycle)',
        labels={'timestamp': 'TimeStamp', 'temperature': 'Temperature [deg.C]'}
    )
    
    # x軸ラベルを90度回転（日時表示が長く重なってしまうのを防ぐ）
    fig.update_xaxes(tickangle=90)  

    # 作成したグラフオブジェクトを返し、Web画面上の 'live-graph' に反映
    return fig

# アプリケーションの実行
# Run the app（このPythonファイルが直接実行された場合にWebサーバーを起動）
if __name__ == '__main__':
    app.run(debug=False)
