# 1. ライブラリ・モジュールのインポート
# DB関連をまとめた自作モジュール（DB接続やデータ取得関数を管理）
import db_ambient_count02

# データフレーム形式で表データを効率的に扱うためのPandas
import pandas as pd

# 可視化用のグラフ描画ライブラリ（Plotly Express）
import plotly.express as px

# Dashでゲージ、LED、インジケータなどの高度なUI部品を使うためのライブラリ
import dash_daq as daq

# Webアプリケーション作成用ライブラリ (Dash)
from dash import Dash, dcc, html, dash_table, Output, Input

# 日付を扱うための標準ライブラリ
from datetime import date

# 2. アプリケーションの初期化
# Dashアプリケーションインスタンスの生成
app = Dash()

# 3. ダッシュボードのレイアウト定義 (UI設計)
# アプリケーション全体のHTML構造を定義
app.layout = html.Div([
    # ==========================================
    # 3-0. 【自動更新タイマ】5秒ごとにコールバックをトリガ
    # ==========================================
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # 5000ミリ秒 = 5秒
        n_intervals=0       # 起動からのカウント初期値
    ),
    
    # ==========================================
    # 3-1. 【左側】サイドバー（コントロールパネル）
    # ==========================================
    html.Div([
        # サイドバー上部のタイトル
        html.H2("Control Panel", style={'color': 'white', 'marginBottom': '30px', 'fontSize': '20px'}),
    
        # --- ① ノード表示・非表示切替（ドロップダウン / 複数選択可） ---
        html.P("表示ノード選択", style={'color': 'white', 'fontWeight': 'bold', 'fontSize': '12px', 'marginBottom': '8px'}),
        dcc.Dropdown(
            id='node-dropdown',
            options=[
                {"label": "Raspberry Pi BME280", "value": "tochigi_iot_0XX"},
                {"label": "ESP32-DevKitC-VE BME280", "value": "tochigi_mqtt_0XX"},
            ],
            value="tochigi_iot_0XX",  # 初期選択値
            clearable=False,          # 選択をクリアできないようにする設定
            style={'marginBottom': '25px', 'color': 'black'}
        ),
        
        # --- ② 気温・湿度切り替え（ラジオボタン） ---
        html.P("折れ線グラフの表示", style={'color': 'white', 'fontWeight': 'bold', 'fontSize': '12px', 'marginBottom': '8px'}),
        dcc.RadioItems(
            id='metric-radio',
            options=[
                {"label": " 温度 (Temperature)", "value": "temperature"},
                {"label": " 湿度 (Humidity)", "value": "humidity"},
            ],
            value="temperature",      # 初期選択値
            style={'marginBottom': '25px', 'fontSize': '13px'}
        ),
        
        # --- ③ 折れ線グラフのサンプル数調整（スライダ） ---
        html.P("折れ線グラフのサンプル数", style={'color': 'white', 'fontWeight': 'bold', 'fontSize': '12px', 'marginBottom': '8px'}),
        dcc.Slider(
            id='limit-slider',
            min=5,
            max=100,
            value=50,
            updatemode="drag",        # ドラッグ中にリアルタイム更新
            marks={5: '5', 50: '50', 100: '100'},
        ),
        
        # --- ④ 日付選択ピッカー ---
        html.P("日付選択", style={'color': 'white', 'fontWeight': 'bold', 'fontSize': '12px', 'marginBottom': '8px'}),
        dcc.DatePickerSingle(
            id='date-picker',
            date=date(2026, 4, 1)    # 初期選択日
        ), 
    ], style={
        'width': '200px',
        'backgroundColor': '#1e1e2f',
        'padding': '25px 20px',
        'height': '100vh', 
        'overflowY': 'auto',          # サイドバー内が長い場合にスクロール可能にする
        'boxSizing': 'box-sizing'
    }),
    
    # ==========================================
    # 3-2. 【右側】メインコンテンツエリア
    # ==========================================
    html.Div([
        # メインヘッダ（タイトル）
        html.H1("Environmental Monitoring", style={'color': 'black', 'marginTop': '1px', 'marginBottom': '10px', 'fontSize': '40px', 'fontWeight': 'bold'}),
        
        # --- 上段：各種ゲージ ＆ LEDディスプレイ ---
        html.Div([
            # 1. 温度ゲージ ＆ LED
            html.Div([
                html.P("Temperature Gauge", style={'color': 'black', 'fontSize': '12px', 'fontWeight': 'bold'}),
                daq.Gauge(
                    id='gauge-temp',
                    label="Temp [deg.C]",
                    min=0.0,
                    max=40.0,
                    value=0,
                    size=130,
                    color="red",
                    showCurrentValue=True,
                    units="deg.C"
                ),
                daq.LEDDisplay(
                    id='led-temp',
                    value="0.0",
                    size=30,
                    color="red"
                )
            ], style={
                'backgroundColor': 'white',
                'width': '50px',
                'height': '350px',
                'padding': '5px',
                'borderRadius': '8px',
                'flex': '1',
                'textAlign': 'center',
            }),
            
            # 2. 湿度ゲージ ＆ LED
            html.Div([
                html.P("Humidity Gauge", style={'color': 'black', 'fontSize': '12px', 'fontWeight': 'bold'}),
                daq.Gauge(
                    id='gauge-humi',
                    label="Humi [%]",
                    min=0.0,
                    max=100.0,
                    value=0,
                    size=130,
                    color="blue",
                    showCurrentValue=True,
                    units="%"
                ),
                daq.LEDDisplay(
                    id='led-humi',
                    value="0.0",
                    size=30,
                    color="blue"
                )
            ], style={
                'backgroundColor': 'white',
                'width': '50px',
                'height': '350px',
                'padding': '5px',
                'borderRadius': '8px',
                'flex': '1',
                'textAlign': 'center',
            }),
            
            # 3. 気圧ゲージ ＆ LED
            html.Div([
                html.P("Pressure Gauge", style={'color': 'black', 'fontSize': '12px', 'fontWeight': 'bold'}),
                daq.Gauge(
                    id='gauge-press',
                    label="Press [hPa]",
                    min=800.0,
                    max=1100.0,
                    value=0,
                    size=130,
                    color="green",
                    showCurrentValue=True,
                    units="hPa"
                ),
                daq.LEDDisplay(
                    id='led-press',
                    value="0.0",
                    size=30,
                    color="green"
                )
            ], style={
                'backgroundColor': 'white',
                'width': '50px',
                'height': '350px',
                'padding': '5px',
                'borderRadius': '8px',
                'flex': '1',
                'textAlign': 'center',
            }),
        ], style={
            'display': 'flex',
            'gap': '5px',
            'marginBottom': '10px'
        }),
        
        # --- 中段：スライダ連動・ラジオボタン切替の折れ線グラフ（トレンド） ---
        html.Div([
            dcc.Graph(id='line-trend-graph')
        ], style={
            'backgroundColor': 'white',
            'padding': '5px',
            'borderRadius': '8px',
            'marginBottom': '10px'
        }),
        
        # --- 下段：DatePickerSingle連動の24時間平均気温（または湿度）棒グラフ ---
        html.Div([
            dcc.Graph(id='hourly-bar-graph')
        ], style={
            'backgroundColor': 'white',
            'padding': '5px',
            'borderRadius': '8px',
            'marginBottom': '10px'
        }), 
        
        # --- 最下段：直近の測定データを表示するデータテーブルエリア ---
        html.Div([
            html.Div(id='table-container')
        ], style={
            'backgroundColor': 'white',
            'padding': '5px',
            'borderRadius': '5px',
            'marginBottom': '5px'
        }),
    ], style={
        'flex': '1',
        'padding': '10px', 
        'backgroundColor': 'white', 
        'height': '100vh',
        'overflowY': 'auto',          # メインコンテンツが長くなった場合にスクロール可能にする
        'boxSizing': 'box-sizing',
    })
], style={
    "display": "flex",
    "height": "100vh",
    "overflow": "hidden",             # 画面全体のスクロールを抑制し、左右それぞれのスクロールに任せる
    "margin": "0"
})

# 4. コールバック処理（UI操作 ＋ 5秒自動更新タイマに連動）
@app.callback(
    Output('gauge-temp', 'value'),
    Output('gauge-humi', 'value'),
    Output('gauge-press', 'value'),
    Output('led-temp', 'value'),
    Output('led-humi', 'value'),
    Output('led-press', 'value'),
    Output('line-trend-graph', 'figure'),
    Output('hourly-bar-graph', 'figure'),
    Output('table-container', 'children'),
    Input('node-dropdown', 'value'),
    Input('metric-radio', 'value'),
    Input('limit-slider', 'value'),
    Input('date-picker', 'date'),
    Input('interval-component', 'n_intervals')
)
def update_dashboard(selected_nodes, metric, limit_count, selected_date, n_intervals):
    """
    サイドバーの各種UI操作、または5秒ごとのタイマー経過（n_intervalsの更新）を検知して実行され、
    データベースから最新データを取得してダッシュボード全体を再描画するメインのコールバック関数。
    """
    # ----------------------------------------------------
    # ステップ1: データベースへの接続確立
    # ----------------------------------------------------
    db_ambient_count02.connect()

    # ----------------------------------------------------
    # ステップ2: 指定ノードIDと件数条件で最新データをクエリ
    # ----------------------------------------------------
    result = db_ambient_count02.select_newest(selected_nodes, limit_count)

    # ----------------------------------------------------
    # ステップ3: 取得したデータを表形式（Pandas DataFrame）に変換
    # ----------------------------------------------------
    df = pd.DataFrame(result)
    print(df) # デバッグ用：取得した直近データをコンソール出力
    
    # 最新の1件目から各環境センサーの現在値を抽出
    current_temp = df.iloc[0]["temperature"]
    current_humi = df.iloc[0]["humidity"]
    current_press = df.iloc[0]["pressure"]
    
    # ----------------------------------------------------
    # ステップ4: 棒グラフ用データ（DatePickerSingle連動：1時間毎の平均データ）の取得
    # ----------------------------------------------------
    datetime_start = f'{selected_date} 00:00:00'
    ave_result = db_ambient_count02.select_ave_one_hour(selected_nodes, datetime_start, 24)
    df_ave = pd.DataFrame(ave_result)
    print(df_ave) # デバッグ用：1時間ごとの平均データをコンソール出力

    # ----------------------------------------------------
    # ステップ5: テーブル表示用データの抽出（最新上位10件）
    # ----------------------------------------------------
    df_tb = df.head(10)
    print(df_tb) # デバッグ用：テーブル用データをコンソール出力
    
    # ----------------------------------------------------
    # ステップ6: ラジオボタンの選択値（metric）に応じたグラフ生成
    # ----------------------------------------------------
    if metric == 'temperature':
        # --- 【気温選択時】折れ線グラフ（赤色）の作成 ---
        fig_line = px.line(
            df,
            x='timestamp',   # X軸: 日時
            y='temperature', # Y軸: 気温
            title=f'Temperature Trend (Node: {selected_nodes})',
            labels={'timestamp': 'TimeStamp', 'temperature': 'Temperature [deg.C]'},
            color_discrete_sequence=['red']  # 折れ線の色を赤に指定
        )
        # --- 【気温選択時】時間別平均棒グラフの作成 ---
        fig_bar = px.bar(
            df_ave,
            x='timestamp',
            y='temperature',
            title=f'Latest Temperature Trend for {selected_nodes}',
            labels={'timestamp': 'TimeStamp', 'temperature': 'AVG.Temperature [deg.C]'}
        )
    else:
        # --- 【湿度選択時】折れ線グラフ（青色）の作成 ---
        fig_line = px.line(
            df,
            x='timestamp',   # X軸: 日時
            y='humidity',    # Y軸: 湿度
            title=f'Humidity Trend (Node: {selected_nodes})',
            labels={'timestamp': 'TimeStamp', 'humidity': 'Humidity [%]'},
            color_discrete_sequence=['blue']  # 折れ線の色を青に指定
        )
        # --- 【湿度選択時】時間別平均棒グラフの作成 ---
        fig_bar = px.bar(
            df_ave,
            x='timestamp',
            y='humidity',
            title=f'Latest Humidity Trend for {selected_nodes}',
            labels={'timestamp': 'TimeStamp', 'humidity': 'AVG.Humidity [%]'}
        )

    # ----------------------------------------------------
    # ステップ7: データテーブルコンポーネントの構築とデザイン設定
    # ----------------------------------------------------
    data_table = dash_table.DataTable(
        # テーブルの列（カラム名）を動的に設定
        columns=[{"name": i, "id": i} for i in df_tb.columns],

        # テーブルの中身（レコードの辞書形式データ）を設定
        data=df_tb.to_dict("records"),
        
        # ヘッダー部分のデザイン設定（中央揃え、フォントサイズ、背景・文字色）
        style_header={
            "textAlign": "center", 
            "fontSize": 15, 
            "backgroundColor": "gray",
            "color": "white"
        },
        
        # データセル部分のデザイン設定（左揃え、フォントサイズ）
        style_data={
            "textAlign": "left", 
            "fontSize": 13
        },
        
        # 条件付き書式の設定（例: 気温 temperature が 28.0 を超える行の該当セルを赤色にする）
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
    )
    
    # ----------------------------------------------------
    # ステップ8: すべての出力コンポーネントへ結果を一括返却
    # ----------------------------------------------------
    return current_temp, current_humi, current_press, str(current_temp), str(current_humi), str(current_press), fig_line, fig_bar, data_table

# 5. アプリケーションの実行
# このスクリプトが直接実行された場合にのみWebサーバを起動する
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8050, debug=False)