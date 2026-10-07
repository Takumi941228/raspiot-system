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


# ==========================================
# 3. ダッシュボードレイアウトの定義
# ==========================================

# ダッシュボードレイアウトの変更（Web
