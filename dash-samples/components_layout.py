# ==========================================
# 1. ライブラリ・モジュールの読み込み (インポート)
# ==========================================
# DB関連をまとめたモジュール（自作モジュール：DBへの接続やデータ取得関数を管理）
import db_ambient_count02

# データフレームという表形式でデータを扱うためのPandas
import pandas as pd

# グラフ描画用ライブラリ（Plotly Express）
import plotly.express as px

# Dashでゲージ、LED、インジケータなどの高度なUI部品を使うためのライブラリ
import dash_daq as daq

# Webアプリケーション作成用ライブラリ (Dash)
# - Dash: アプリケーション本体
# - dcc (Dash Core Components): ドロップダウン、スライダ、カレンダー、タイマ、グラフなどのUI部品
# - html (Dash HTML Components): HTMLタグやCSSレイアウトを作る部品
# - dash_table: リッチな表を表示・操作するための部品
# - Output, Input: ユーザ操作や時間経過に応じて画面を動的に更新するための仕組み
from dash import Dash, dcc, html, dash_table, Output, Input

# 日付を扱うための標準ライブラリ
from datetime import date

# ==========================================
# 2. アプリの初期化
# ==========================================
app = Dash()

# ==========================================
# 3. ダッシュボードのレイアウト定義 (UI設計)
# ==========================================
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
        # ダッシュボードタイトル
        html.H2("IoT Control Panel", style={'color': 'white', 'marginBottom': '30px', 'fontSize': '20px', 'letterSpacing': '1px'}),
    
        # --- ① ノード表示・非表示切替（ドロップダウン / 複数選択可） ---
        html.Label("表示ノード選択 (Nodes):", style={'color': '#adb5bd', 'fontWeight': 'bold', 'fontSize': '12px', 'display': 'block', 'marginBottom': '8px'}),
        dcc.Dropdown(
            id='node-dropdown',
            options=[
                {"label": "Raspberry Pi (tochigi_iot_018)", "value": "tochigi_iot_018"},
                {"label": "ESP32-DevKit (tochigi_mqtt_018)", "value": "tochigi_mqtt_018"},
            ],
            value=["tochigi_iot_018", "tochigi_mqtt_018"],  # 初期は両方表示
            multi=True,  # 複数選択（表示・非表示の切り替え）に対応
            style={'marginBottom': '25px', 'color': '#333'}
        ),
        # --- ② 気温・湿度切り替え（ラジオボタン） ---
        html.Label("折れ線グラフの表示指標:", style={'color': '#adb5bd', 'fontWeight': 'bold', 'fontSize': '12px', 'display': 'block', 'marginBottom': '8px'}),
        dcc.RadioItems(
            id='metric-radio',
            options=[
                {"label": " 温度 (Temperature)", "value": "temperature"},
                {"label": " 湿度 (Humidity)", "value": "humidity"},
            ],
            value="temperature",  # 初期選択
            style={'color': 'white', 'marginBottom': '25px', 'lineHeight': '2.2', 'fontSize': '13px'}
        ),
        # --- ③ 折れ線グラフのサンプル数調整（スライダ） ---
        html.Label("折れ線グラフ サンプル数:", style={'color': '#adb5bd', 'fontWeight': 'bold', 'fontSize': '12px', 'display': 'block', 'marginBottom': '8px'}),
        dcc.Slider(
            id='limit-slider',
            min=5,
            max=200,
            value=20,
            updatemode="drag",
            marks={5: '5', 100: '100', 200: '200'},
            #style={'marginBottom': '25px'}
        ),
        # --- ④ 日付選択（DatePickerSingle / 24時間平均棒グラフ用） ---
        html.Label("棒グラフ対象日 (1時間平均):", style={'color': '#adb5bd', 'fontWeight': 'bold', 'fontSize': '12px', 'display': 'block', 'marginBottom': '8px'}),
        dcc.DatePickerSingle(
            id='date-picker',
            date=date(2026, 10, 18),  # 初期日付
            style={'marginBottom': '20px'}
        ),
    ], style={
        'width': '300px',
        'backgroundColor': '#1e1e2f',  # ダークトーンのサイドバー
        'padding': '25px 20px',
        'height': '100vh', 
        'position': 'fixed',
        'left': 0,
        'top': 0,
        'boxSizing': 'box-sizing',
        'fontFamily': 'sans-serif',
        'overflowY': 'auto',
        'boxShadow': '2px 0 5px rgba(0,0,0,0.1)'
    }),
    # ==========================================
    # 3-2. 【右側】メインコンテンツエリア
    # ==========================================
    html.Div([
        # メインヘッダ
        html.H1("IoT Environmental Monitoring Dashboard", style={'color': '#2c3e50', 'marginBottom': '20px', 'fontSize': '22px', 'fontWeight': '600'}),
        # --- 上段：ゲージ、LEDディスプレイ、警告インジケータ
        html.Div([
            # 1. 温度ゲージ ＆ LED
            html.Div([
                html.P("Temperature Monitor", style={'margin': '0 0 5px 0', 'color': '#7f8c8d', 'fontSize': '12px', 'fontWeight': 'bold'}),
                daq.Gauge(id='gauge-temp', min=0, max=50, value=0, label="Temp [°C]", color="#e74c3c", size=130, scale={'start': 0, 'interval': 10, 'labelInterval': 2}),
                daq.LEDDisplay(id='led-temp', value="0.0", size=20, color="#e74c3c", style={'marginTop': '10px'})
            ], style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.04)', 'flex': '1', 'textAlign': 'center', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
            # 2. 湿度ゲージ ＆ LED
            html.Div([
                html.P("Humidity Monitor", style={'margin': '0 0 5px 0', 'color': '#7f8c8d', 'fontSize': '12px', 'fontWeight': 'bold'}),
                daq.Gauge(id='gauge-humi', min=0, max=100, value=0, label="Humi [%]", color="#3498db", size=130, scale={'start': 0, 'interval': 20, 'labelInterval': 1}),
                daq.LEDDisplay(id='led-humi', value="0.0", size=20, color="#3498db", style={'marginTop': '10px'})
            ], style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.04)', 'flex': '1', 'textAlign': 'center', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
            # 3. 気温28度超えアラート インジケータ
            html.Div([
                html.P("Temperature Alert", style={'margin': '0 0 15px 0', 'color': '#7f8c8d', 'fontSize': '12px', 'fontWeight': 'bold'}),
                daq.Indicator(
                    id='alert-indicator',
                    value=False,
                    label="Normal (< 28°C)",
                    color="#2ecc71",
                    size=30
                ),
                html.P("Threshold: 28.0°C", style={'margin': '15px 0 0 0', 'color': '#95a5a6', 'fontSize': '11px'})
            ], style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.04)', 'flex': '1', 'textAlign': 'center', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center'}),
        ], style={'display': 'flex', 'gap': '15px', 'marginBottom': '20px'}),
        # --- 中段：スライダ連動・ラジオボタン切替の折れ線グラフ（複数ノード対応） ---
        html.Div([
            dcc.Graph(id='line-trend-graph')
        ], style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.04)', 'marginBottom': '20px'}),
        # --- 下段左：DatePickerSingle連動の24時間平均気温棒グラフ ---
        html.Div([
            dcc.Graph(id='hourly-bar-graph')
        ], style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.04)', 'marginBottom': '20px'}),
        
        # --- 下段右：最新データ10個分のテーブル表示 ---
        html.Div([
            html.H3("Latest 10 Records", style={'fontSize': '16px', 'color': '#2c3e50', 'marginBottom': '10px'}),
            html.Div(id='table-container')
        ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.04)', 'marginBottom': '30px'}),
    ], style={
        'marginLeft': '300px',  # サイドバーの幅分だけ右に余白をとる
        'padding': '25px', 
        'backgroundColor': '#f4f6f9', 
        'minHeight': '100vh', 
        'boxSizing': 'box-sizing',
        'fontFamily': 'sans-serif'
    })
])

# ==========================================
# 4. コールバック処理（UI操作 ＋ 5秒自動更新タイマに連動）
# ==========================================
@app.callback(
    [
        Output('gauge-temp', 'value'),
        Output('gauge-humi', 'value'),
        Output('led-temp', 'value'),
        Output('led-humi', 'value'),
        Output('alert-indicator', 'value'),
        Output('alert-indicator', 'label'),
        Output('alert-indicator', 'color'),
        Output('line-trend-graph', 'figure'),
        Output('hourly-bar-graph', 'figure'),
        Output('table-container', 'children')
    ],
    [
        Input('node-dropdown', 'value'),
        Input('metric-radio', 'value'),
        Input('limit-slider', 'value'),
        Input('date-picker', 'date'),
        Input('interval-component', 'n_intervals')  # ← 5秒ごとのタイマ発火をトリガに追加
    ]
)
def update_dashboard(selected_nodes, metric, limit_count, selected_date, n_intervals):
    """
    サイドバーのUI操作、または5秒ごとのタイマー経過を検知して実行され、
    データベースから最新データを取得してダッシュボード全体を再描画する関数
    """
    # 1. データベース接続
    db_ambient_count02.connect()
    # ----------------------------------------------------
    # A. 基準となるプライマリノードの選定（最初の選択ノード、未選択ならデフォルト）
    # ----------------------------------------------------
    if not selected_nodes:
        primary_node = "tochigi_iot_018"
    else:
        primary_node = selected_nodes[0]
    # 最新データの取得（ゲージ、LED、インジケータ、テーブル用）
    newest_result = db_ambient_count02.select_newest(primary_node, 10)
    df_newest = pd.DataFrame(newest_result)
    # 現在値の抽出
    current_temp = float(df_newest.iloc[0]["temperature"]) if not df_newest.empty else 0.0
    current_humi = float(df_newest.iloc[0]["humidity"]) if not df_newest.empty else 0.0

    # 28度超えインジケータの判定
    is_hot = bool(current_temp > 28.0)
    alert_label = "Alert (> 28°C)" if is_hot else "Normal (< 28°C)"
    alert_color = "#e74c3c" if is_hot else "#2ecc71"

    # ----------------------------------------------------
    # B. 折れ線グラフ用データ（複数ノードの表示・非表示＆スライダ件数対応）
    # ----------------------------------------------------
    line_dfs = []
    if selected_nodes:
        for node in selected_nodes:
            res = db_ambient_count02.select_newest(node, limit_count)
            df_node = d.DataFrame(res)
            if not df_node.empty:
                df_node['node_id'] = node  # ノード識別列を追加
                line_dfs.append(df_node)
    if line_dfs:
        df_line = pd.concat(line_dfs, ignore_index=True)
    else:
        df_line = pd.DataFrame(columns=['timestamp', 'temperature', 'humidity', 'node_id'])
    # Plotlyでマルチノード折れ線グラフ作成
    metric_label = "Temperature [deg.C]" if metric == 'temperature' else "Humidity [%]"
    fig_line = px.line(
        df_line,
        x='timestamp',
        y=metric,
        color='node_id' if 'node_id' in df_line.columns else None,
        title=f'Trend Analysis ({metric.capitalize()}) - Auto Updated',
        labels={'timestamp': 'TimeStamp', metric: metric_label, 'node_id': 'Node'}
    )
    fig_line.update_layout(template='plotly_white', margin=dict(t=40, b=40, l=40, r=40))
    
    # ----------------------------------------------------
    # C. 棒グラフ用データ（DatePickerSingle連動：1時間毎の平均気温24本）
    # ----------------------------------------------------
    datetime_start = f'{selected_date} 00:00:00'
    ave_result = db_ambient_count02.select_ave_one_hour(primary_node, datetime_start, 24)
    df_ave = pd.DataFrame(ave_result)

    fig_bar = px.bar(
        df_ave,
        x='timestamp',
        y='temperature',
        title=f'Hourly Average Temperature ({primary_node} on {selected_date})',
        labels={'timestamp': 'TimeStamp', 'temperature': 'AVG-Temperature [deg.C]'},
        color_discrete_sequence=['#3498db']
    )
    fig_bar.update_layout(template='plotly_white', margin=dict(t=40, b=40, l=40, r=40))
    
    # ----------------------------------------------------
    # D. テーブル用データ（最新10件）
    # ----------------------------------------------------
    table_component = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in df_newest.columns],
        data=df_newest.to_dict("records"),
        style_header={"textAlign": "center", "fontSize": 12, "backgroundColor": "#34495e", "color": "white", "fontWeight": "bold"},
        style_data={"textAlign": "left", "fontSize": 11, "backgroundColor": "white"},
        style_data_conditional=[
            {"if": {"column_id": "temperature", "filter_query": "{temperature} > 28.0"}, "backgroundColor": "#fadbd8", "color": "#900c3f"}
        ],
        page_size=10
    )
    
    # すべての出力コンポーネントへ結果を返す
    return (
        current_temp, 
        current_humi, 
        str(current_temp), 
        str(current_humi),
        is_hot,
        alert_label,
        alert_color,
        fig_line,
        fig_bar,
        table_component
    )

# ==========================================
# 5. アプリケーションの実行
# ==========================================
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(debug=False)