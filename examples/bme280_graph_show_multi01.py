#DB関連をまとめたモジュール
import db_ambient_count02

#グラフ表示に関するライブラリ
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def main():
    #DBサーバに接続する
    db_ambient_count02.connect()

    #クエリのパラメータを入力
    #表示を開始する日付・時刻を入力する
    print('最新のデータを表示します。')
    print('どのノードのデータを表示しますか？')

    node_id = input('ノードの Identifier(例: tochigi_mqtt_999): ')

    print('何サンプル前のデータまで表示しますか？')
    #入力したデータを数値に変換
    limit_count = int(input('数値を入力(例: 100) : '))

    #クエリを実施して結果を得る
    result = db_ambient_count02.select_newest(node_id, limit_count)

    #結果を表形式に変換する
    df = pd.DataFrame(result)

    #コンソール表示
    print(df)

    #３行×１列の描画領域の作成
    fig = make_subplots(rows=3, cols=1)

    #traceの登録
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["temperature"], name='Temperature'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["humidity"], name='Humidity'), row=2, col=1)
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["pressure"], name='Pressure'), row=3, col=1)

    #グラフの調整
    #Update xaxis properties
    fig.update_xaxes(title_text="TimeStamp", row=1, col=1)
    fig.update_xaxes(title_text="TimeStamp", row=2, col=1)
    fig.update_xaxes(title_text="TimeStamp", row=3, col=1)

    #Update yaxis properties
    fig.update_yaxes(title_text="Temperature [deg. C.]",row=1, col=1)
    fig.update_yaxes(title_text="Humidity [%]",row=2, col=1)
    fig.update_yaxes(title_text="Pressure [hPa]",row=3, col=1)

    #Update title
    fig.update_layout(title_text = f'Latest E Trend for {node_id}')
    
    fig.show()

if __name__ == '__main__':
    main()