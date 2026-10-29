# ==============================================================================
# 【プログラム概要】
# このスクリプトは、自作のDBモジュールと連携して1時間ごとの平均温度データを取得し、
# DashおよびPlotly Expressを使用してWebブラウザ上でグラフとして可視化する
# Webアプリケーションです。
# ユーザはコンソール（ターミナル）からの対話形式で、対象のノードIDや
# データの取得開始日時、行数を指定することができます。
# ==============================================================================

# 1. ライブラリ・モジュールの読み込み (インポート)
import db_ambient_count02  # DBへの接続やデータ取得関数を管理する自作モジュール
import pandas as pd        # 表形式のデータを効率的に扱うためのライブラリ
import plotly.express as px  # 直感的な操作で高度なグラフを作成できるライブラリ
from dash import Dash, dcc   # Webアプリの構築(Dash)およびUI部品(dcc)

# 2. アプリの初期化とデータベース接続
app = Dash()                    # Dashアプリケーションのインスタンス生成
db_ambient_count02.connect()    # データベースサーバへ接続

# 3. ターミナルからのパラメータ入力
print('１時間ごとに平均したデータを表示します。')
print('どのノードのデータを表示しますか？')
node_id = input('ノードのIdentifier(例: tochigi_mqtt_0XX): ')

print('いつのデータから表示しますか？')
s_year = input('年(例: 2026): ')
s_month = input('月(例: 10): ')
s_day = input('日(例: 01): ')
s_hour = input('時(例: 00): ')
datetime_start = f'{s_year}-{s_month}-{s_day} {s_hour}:00:00'

print(f'{datetime_start}のデータから何行のデータを表示しますか？')
limit_count = int(input('数値を入力(例: 24) : '))  # 入力文字列を整数に変換

# 4. データの取得と整形
# 指定されたパラメータをもとにデータベースからデータを抽出
result = db_ambient_count02.select_ave_one_hour(node_id, datetime_start, limit_count)

# 取得した結果を表形式（Pandas DataFrame）に変換
df = pd.DataFrame(result)

# コンソールに取得したデータフレームの内容を出力して確認
print(df)

# 5. ダッシュボードレイアウトの定義
# Plotlyの棒グラフを作成し、Dashアプリのレイアウトとして設定
app.layout = dcc.Graph(
    figure=px.bar(
        df,
        x='timestamp',
        y='temperature',
        title=f'Latest Temperature Trend for {node_id}',
        labels={'timestamp': 'TimeStamp', 'temperature': 'AVG.Temperature [deg.C]'}
    )
)

# 6. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8050, debug=False)