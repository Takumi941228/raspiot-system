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
    dcc
