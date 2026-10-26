# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashとPlotly Expressを使用して、指定したセンサノードの
# 最新の温度データをデータベースから取得し、Webブラウザ上で折れ線グラフとして
# 可視化するシンプルなWebアプリケーションです。
# ユーザは起動時にターミナルから対象のノードIDと取得するサンプル数（行数）を入力します。
# ==============================================================================

# 1. ライブラリ・モジュールの読み込み (インポート)
# DB関連をまとめたモジュール（自作モジュール：DBへの接続やデータ取得関数を管理）
import db_ambient_count02

# グラフ表示に関するライブラリ（データフレームという表形式でデータを扱うためのPandas）
import pandas as pd

# グラフ描画用ライブラリ（直感的な操作で高度なグラフを描画できるPlotly Express）
import plotly.express as px

# Webアプリケーション作成用ライブラリ (Dash)
# - Dash: アプリケーション本体を作成
# - dcc (Dash Core Components): グラフ描画エリアなどのUI部品
from dash import Dash, dcc

# 2. アプリの初期化とデータベース接続
# アプリの初期化
app = Dash()

# データベースサーバに接続
db_ambient_count02.connect()

# 3. ターミナルからのパラメータ入力
print('最新のデータを表示します。')
print('どのノードのデータを表示しますか？')
node_id = input('ノードの Identifier (例: tochigi_mqtt_0XX): ')

print('何サンプル前のデータまで表示しますか？')
# 入力したデータを数値（整数）に変換
limit_count = int(input('数値を入力 (例: 10) : '))

# 4. データの取得と整形
# 指定された条件でデータベースから最新データをクエリ（検索実行）
result = db_ambient_count02.select_newest(node_id, limit_count)

# 取得した結果を表形式（Pandas DataFrame）に変換する
df = pd.DataFrame(result)

# 動作確認のため、コンソールにデータフレームの内容を表示
print(df)

# 5. ダッシュボードのレイアウト定義 (UI設計)
# 取得したDataFrameをもとに、Plotlyで折れ線グラフを作成し、アプリのレイアウトに設定
app.layout = dcc.Graph(
    figure=px.line(
        df,
        x='timestamp',   # X軸: 日時
        y='temperature', # Y軸: 気温
        title=f'Latest Temperature Trend for {node_id}',
        labels={'timestamp': 'TimeStamp', 'temperature': 'Temperature [deg.C]'}
    )
)

# 6. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(debug=False)