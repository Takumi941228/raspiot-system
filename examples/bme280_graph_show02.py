#DB関連をまとめたモジュール
import db_ambient_count02

#グラフ表示に関するライブラリ
import pandas as pd
import plotly.express as px

def main():
    #DBサーバに接続する
    db_ambient_count02.connect()

    #クエリのパラメータを入力
    #表示を開始する日付・時刻を入力する
    print('最新のデータを表示します。')
    print('どのノードのデータを表示しますか？')
    node_id = input('ノードの Identifier(例:tochigi_mqtt_999): ')

    print('何サンプル前のデータまで表示しますか？')
    #入力したデータを数値に変換
    limit_count = int(input('数値を入力(例: 10) : '))

    #クエリを実施して結果を得る
    result = db_ambient_count02.select_newest(node_id, limit_count)

    #結果を表形式に変換する
    df = pd.DataFrame(result)

    # コンソール表示（任意）
    print(df)

    # Plotlyで折れ線グラフ
    fig = px.line(
        df,
        x='timestamp',
        y='temperature',
        title=f'Latest Temperature Trend for {node_id}',
        labels={'timestamp': 'TimeStamp', 'temperature': 'Temperature [deg.C]'}
    )


    fig.update_xaxes(tickangle=90)  #x軸ラベルを90度回転
    fig.show()

if __name__ == '__main__':
    main()