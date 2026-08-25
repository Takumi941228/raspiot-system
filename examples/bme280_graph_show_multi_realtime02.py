#DB関連をまとめたモジュール
import db_ambient_count02

#グラフ表示に関するライブラリ
import pandas as pd
import plotly.express as px

#Webアプリに関するライブラリ
from dash import Dash, dcc, html, callback, Output, Input

#アプリの初期化
app = Dash()

#クエリのパラメータを入力
#表示を開始する日付・時刻を入力する
print('最新のデータをリアルタイムに表示します。')
print('どのノードのデータを表示しますか？')
node_id = input('ノードの Identifier(例: tochigi_iot_999): ')

print('何サンプル前のデータまで表示しますか？')
#入力したデータを数値に変換
limit_count = int(input('数値を入力(例: 20) : '))

print('グラフの更新周期(秒)は？')
#入力したデータを数値に変換
update_cycle = int(input('数値を入力(例: 10) : '))

#ダッシュボードレイアウトの変更
app.layout = html.Div([
    html.H1(children=f"Environmental data"),
    #ドロップダウンボックスの追加
    dcc.Dropdown(
        id='metric-select',
        options=[
            {'label': 'Temperature[deg.C]', 'value':'temperature'},
            {'label': 'Humidity[%]', 'value':'humidity'},
            {'label': 'Pressure[hPa]', 'value':'pressure'}
        ],
        value='temperature' #初期値をtemperatureに設定
    ),
    dcc.Interval(
        id='interval-component',
        interval=update_cycle * 1000,  #ミリ秒単位
        n_intervals=0
    ),
    dcc.Graph(id='live-graph')
])

#自動更新のコールバック内容
@app.callback(
    Output('live-graph', 'figure'),
    Input('interval-component', 'n_intervals'),
    Input('metric-select', 'value')
)

#更新周期毎にグラフの自動描画
def update_graph(n, metric):
    #DBサーバに接続する
    db_ambient_count02.connect()

    #クエリを実施して結果を得る
    result = db_ambient_count02.select_newest(node_id, limit_count)

    #結果を表形式に変換する
    df = pd.DataFrame(result)
 
    #コンソール表示
    print(df)

    #引数metricの値によって描画するグラフを決定
    if metric == 'temperature':
        #グラフ生成
        fig = px.line(
            df,
            x='timestamp',
            y='temperature',
            title=f'Temperature Trend(Node: {node_id}, Every {update_cycle} sec. cycle)',
            labels={'timestamp': 'TimeStamp', 'temperature': 'Temperature [deg.C]'},
            color_discrete_sequence=['red']  #赤に変更
        )
    elif metric == 'humidity':
        #グラフ生成
        fig = px.line(
            df,
            x='timestamp',
            y='humidity',
            title=f'Humidity Trend(Node: {node_id}, Every {update_cycle} sec. cycle)',
            labels={'timestamp': 'TimeStamp', 'humidity': 'Humidity [%]'},
            color_discrete_sequence=['blue']  #青に変更
        )
    else:
        #グラフ生成
        fig = px.line(
            df,
            x='timestamp',
            y='pressure',
            title=f'Pressure Trend(Node: {node_id}, Every {update_cycle} sec. cycle)',
            labels={'timestamp': 'TimeStamp', 'pressure': 'Presuure [hPa]'},
            color_discrete_sequence=['green']  #緑に変更
        )
    
    fig.update_xaxes(tickangle=90)  #x軸ラベルを90度回転

    return fig

#Run the app
if __name__ == '__main__':
    app.run(debug=False)
