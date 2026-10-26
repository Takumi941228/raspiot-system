# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashとカレンダーUI部品（dcc.DatePickerSingle）を使用して、
# ユーザがWebブラウザ上で選択した日付を起点に、1時間ごとの平均温度データを
# データベースから取得し、Plotly Expressの棒グラフでインタラクティブに可視化する
# Webアプリケーションです。
# カレンダーで日付を変更するとコールバックが発火し、自動的にグラフが更新されます。
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
# - dcc (Dash Core Components): カレンダー（DatePickerSingle）やグラフなどのUI部品
# - html (Dash HTML Components): HTMLタグ（枠組みなど）を作成する部品
# - Output, Input: ユーザ操作に応じて画面を動的に更新するための仕組み
from dash import Dash, dcc, html, Output, Input

# 日付を扱うための標準ライブラリ
from datetime import date


# 2. アプリの初期化と起動時パラメータの設定
# アプリの初期化
app = Dash()

# クエリのパラメータをターミナルから事前に入力
print('１時間ごとに平均したデータを表示します。')
print('どのノードのデータを表示しますか？')
node_id = input('ノードの Identifier (例: tochigi_mqtt_0XX): ')

print('何行のデータを表示しますか？')
# 入力したデータを数値（整数）に変換
limit_count = int(input('数値を入力 (例: 24) : '))


# 3. ダッシュボードのレイアウト定義 (UI設計)
# カレンダー（DatePickerSingle）とグラフ描画エリアを配置します
app.layout = html.Div([
    # 【日付選択ピッカ】データを取得したい基準日を選択するためのカレンダー
    dcc.DatePickerSingle(
        id='callback-input',        # コールバックで紐付けるためのID
        date=date(2026, 10, 18)     # 初期選択日付
    ),
    
    # 【グラフ描画エリア】生成したPlotlyグラフを表示する場所
    dcc.Graph(id='live-graph')
])


# 4. コールバック処理（日付変更に連動したグラフの再描画）
# カレンダーで日付が変更された（Inputの変化）のを検知して実行されます。
@app.callback(
    Output('live-graph', 'figure'),         # 【出力】'live-graph' の 'figure' (グラフ画像) を更新
    Input('callback-input', 'date')          # 【入力】カレンダーで選択された日付文字列 (YYYY-MM-DD)
)

def update_graph(data_value):
    """
    カレンダーで選択された日付を受け取り、DBから1時間ごとの平均データを取得して棒グラフを返す関数
    """
    # 1. データベースサーバに接続
    db_ambient_count02.connect()
    
    # 選択された日付に時刻（00:00:00）を結合して開始日時文字列を作成
    datetime_start = f'{data_value} 00:00:00'
    print(f'{datetime_start} のデータから {limit_count} 行分のデータを取得します。')

    # 2. 指定された条件（ノードID、開始日時、行数）でクエリを実施して結果を得る
    result = db_ambient_count02.select_ave_one_hour(node_id, datetime_start, limit_count)
 
    # 3. 取得した結果を表形式（Pandas DataFrame）に変換する
    df = pd.DataFrame(result)
 
    # 動作確認のため、取得したデータをコンソールに表示
    print(df)

    # 4. Plotly Expressを使った棒グラフの生成
    fig = px.bar(
        df,
        x='timestamp',
        y='temperature',
        title=f'Latest Temperature Trend for {node_id}',
        labels={'timestamp': 'TimeStamp', 'temperature': 'AVG.Temperature [deg.C]'}
    )

    # 生成したグラフオブジェクトを返し、画面上の 'live-graph' に反映させる
    return fig

# 5. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(debug=False)