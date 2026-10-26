# ==============================================================================
# 【プログラム概要】
# このスクリプトは、Dashのデータテーブル（dash_table.DataTable）を使用して、
# 指定したセンサーノードのデータベース上の最新データを表形式でWebブラウザ上に
# 美しく、インタラクティブに一覧表示するWebアプリケーションです。
# ユーザーは起動時にターミナルから対象ノードIDとサンプル数を入力します。
# 条件付き書式（temperature > 28.0 のセルを赤色にするなど）のスタイリングも含まれています。
# ==============================================================================

# 1. ライブラリ・モジュールの読み込み (インポート)
# DB関連をまとめたモジュール（自作モジュール：DBへの接続やデータ取得関数を管理）
import db_ambient_count02

# データフレームという表形式でデータを扱うためのPandas
import pandas as pd

# Webアプリケーション作成用ライブラリ (Dash)
# - Dash: アプリケーション本体
# - dash_table: リッチな表（データテーブル）を表示・操作するためのUI部品
from dash import Dash, dash_table

# 2. アプリの初期化と起動時パラメータの設定
# アプリの初期化
app = Dash()

# データベースサーバに接続
db_ambient_count02.connect()

# ターミナルからのパラメータ入力
print('最新のデータを表示します。')
print('どのノードのデータを表示しますか？')
node_id = input('ノードの Identifier (例: tochigi_mqtt_0XX): ')

print('何サンプル前のデータまで表示しますか？')
# 入力したデータを数値（整数）に変換
limit_count = int(input('数値を入力 (例: 10) : '))


# 3. データの取得と整形
# 指定された条件でデータベースから最新データをクエリ（検索実行）
result = db_ambient_count02.select_newest(node_id, limit_count)

# 取得した結果を表形式（Pandas DataFrame）に変換する
df = pd.DataFrame(result)

# 動作確認のため、コンソールにデータフレームを表示
print(df)

# 4. ダッシュボードのレイアウト定義 (UI設計)
# 取得したDataFrameをもとに、インタラクティブなDataTableを作成してレイアウトに設定
app.layout = dash_table.DataTable(
    # テーブルの列（カラム名）を動的に設定
    columns=[{"name": col, "id": col} for col in df.columns],
    
    # テーブルの中身（レコードの辞書形式）
    data=df.to_dict("records"),
    
    # ヘッダ部分のデザイン設定
    style_header={
        "textAlign": "center", 
        "fontSize": 15, 
        "backgroundColor": "gray",
        "color": "white"
    },
    
    # データセル部分のデザイン設定
    style_data={
        "textAlign": "left", 
        "fontSize": 13
    },
    
    # 条件付き書式の設定（例: temperatureが28.0を超える行の該当セルを赤色にする）
    style_data_conditional=[
        {
            "if": {
                "column_id": "temperature", 
                "filter_query": "{temperature} > 28.0"
            }, 
            "backgroundColor": "red",
            "color": "white"
        },
    ],
    
    # ページネーションやスクロール、幅の自動調整などの設定（必要に応じてコメントアウトを解除してください）
    # fill_width=False,
)

# 5. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(debug=False)