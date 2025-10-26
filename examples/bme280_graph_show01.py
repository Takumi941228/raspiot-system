#DB関連をまとめたモジュール
import db_ambient_count01

#グラフ表示に関するライブラリ
import pandas as pd
import plotly.express as px

def main():
    #DBサーバに接続する
    db_ambient_count01.connect()

    #クエリのパラメータを入力
    #表示を開始する日付・時刻を入力する
    print('１時間ごとに平均したデータを表示します。')
    print('どのノードのデータを表示しますか？')
    node_id = input('ノードのIdentifier(例: tochigi_mqtt_999): ')

    print('いつのデータから表示しますか？')
    s_year = input('年(例: 2024): ')
    s_month = input('月(例: 09): ')
    s_day = input('日(例: 19): ')
    s_hour = input('時(例: 00): ')
    datetime_start = f'{s_year}-{s_month}-{s_day} {s_hour}:00:00'
    print(f'{datetime_start}のデータからから何行のデータを表示しますか？')

    #入力したデータを数値に変換
    limit_count = int(input('数値を入力(例: 5) : '))

    #クエリを実施して結果を得る
    result = db_ambient_count01.select_ave_one_hour(node_id, datetime_start, limit_count)

    #結果を表形式に変換する
    df = pd.DataFrame(result)

    #コンソールに表示
    print(df)

    #Plotlyで折れ線グラフ
    fig = px.line(
        df,
        x='timestamp',
        y='temperature',
        title=f'Temperature Trend for {node_id}',
        labels={'timestamp': 'TimeStamp', 'temperature': 'Temperature [deg.C]'}
    )

    fig.update_xaxes(tickangle=90)  #x軸ラベルを90度回転
    fig.show()

if __name__ == '__main__':
    main()