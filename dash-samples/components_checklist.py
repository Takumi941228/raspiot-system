# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashとPlotlyを使用して、複数のセンサノードの温度データを
# Webブラウザ上でインタラクティブに比較・折れ線グラフ表示するWebアプリケーションです。
# 画面上のチェックボックスで表示したいノードを選択すると、コールバック機能により
# 選択状態の変化が検知され、自動的にデータベースから最新データを取得・再描画します。
# ==============================================================================

# 1. ライブラリ・モジュールの読み込み (インポート)
import db_ambient_count02  # DBへの接続やデータ取得関数を管理する自作モジュール
import pandas as pd        # 表形式のデータを効率的に扱うためのライブラリ

# グラフ描画用ライブラリ
import plotly.express as px
import plotly.graph_objects as go  # 複数の線を重ねて描画するために使用

# Webアプリケーション作成用ライブラリ (Dash)
from dash import Dash, dcc, html, Output, Input

# 2. アプリの初期化と起動時パラメータの設定
# アプリの初期化（Dashのインスタンス生成）
app = Dash()

print('最新のデータを表示します。')
print('何サンプル前のデータまで表示しますか？')

# 入力したデータを数値（整数）に変換
limit_count = int(input('数値を入力(例: 100) : '))

# 3. ダッシュボードのレイアウト定義 (UI設計)
# 画面上に配置するチェックボックスとグラフ描画エリアを組み立てます
app.layout = html.Div([
    # 【チェックボックス】表示したいノードを選択するためのUI部品
    dcc.Checklist(
        id='callback-input',  # コールバックで紐付けるためのID
        options=[
            {"label": "Raspberry Pi BME280", "value": "tochigi_iot_0XX"},
            {"label": "ESP32-DevkitC-VE BME280", "value": "tochigi_mqtt_0XX"},
        ],
        value=["tochigi_iot_0XX"]  # 初期状態で選択されているノード
    ),
    
    # 【グラフ描画エリア】生成したPlotlyグラフを表示する場所
    dcc.Graph(id='live-graph')
])

# 4. コールバックの定義 (インタラクティブな処理)
# チェックボックスの選択状態の変化を検知して、グラフを自動で再描画します
@app.callback(
    Output('live-graph', 'figure'),         # 【出力】'live-graph' の 'figure' (グラフ画像) を更新
    Input('callback-input', 'value')        # 【入力】チェックボックスで選択されたノードIDのリスト
)

def update_graph(node_id):
    """
    チェックボックスの選択が変更されたときに実行される関数。
    選択された各ノードの最新データをデータベースから取得し、1つの折れ線グラフにまとめて返します。
    """
    # 1. データベースサーバに接続
    db_ambient_count02.connect()
    
    # 複数ノードの線を重ねて描画するためのグラフオブジェクトを作成
    fig = go.Figure()

    # 選択されたノードを一つずつループしてデータを取得・追加
    for node in node_id:
        print(f"取得件数上限: {limit_count}, 対象ノード: {node}")
        
        # 2. 指定されたノードIDと件数条件で最新データをクエリ（検索実行）
        result = db_ambient_count02.select_newest(node, limit_count)

        # 3. 取得したデータをPandasのデータフレーム（表形式）に変換
        df = pd.DataFrame(result)
 
        # 動作確認のため、取得したデータをコンソールに表示
        print(df)

        # 4. グラフにトレース（線データ）を追加
        fig.add_trace(go.Scatter(
            x=df["timestamp"], 
            y=df["temperature"], 
            mode='lines+markers',
            name=str(node)
        ))

    # 5. グラフのデザイン調整・レイアウト設定
    fig.update_xaxes(title_text="TimeStamp")
    fig.update_yaxes(title_text="Temperature [deg. C.]")
    fig.update_layout(title_text='Latest Temperature Trend')

    # 生成したグラフオブジェクトを返し、画面上の 'live-graph' に反映させる
    return fig

# 6. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(debug=False)