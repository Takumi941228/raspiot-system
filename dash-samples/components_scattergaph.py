# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashとPlotly Expressの散布図（px.scatter）を使用して、
# 指定したセンサノードの最新データから「気温」と「湿度」の関係性を
# Webブラウザ上で可視化するシンプルなWebアプリケーションです。
# ユーザは起動時にターミナルから対象のノードIDと取得するサンプル数（行数）を入力します。
# X軸に気温、Y軸に湿度をとることで、温湿度の相関や分布を直感的に把握できます。
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

# 5. ダッシュボードレイアウトの定義 (UI設計)
# 取得したDataFrameをもとに、Plotlyで散布図（Scatter plot）を作成し、アプリのレイアウトに設定
app.layout = dcc.Graph(
    figure=px.scatter(
        df,
        x='temperature',  # X軸: 気温 [deg.C]
        y='humidity',     # Y軸: 湿度 [%]
        title=f'Trend for {node_id}',  # タイトル
        labels={
            'temperature': 'Temperature [deg.C]', 
            'humidity': 'Humidity [%]'
        }
    )
)

# 6. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(debug=False)