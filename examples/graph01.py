# pandasに関するライブラリを使用する
import pandas as pd

# Plotlyに関数ライブラリを使用する。
import plotly.express as px

# 折れ線グラフを作成
fig = px.line(
    # 横軸（x軸）のデータを指定（曜日）
    x=["Mon", "Tue", "Wed", "Thu", "Fri"],

    # 縦軸（y軸）のデータを指定（温度）
    y=[10, 20, 15, 25, 30],

    # グラフのタイトルを設定
    title="1週間の温度変化"
)

# 作成したグラフを表示（ブラウザ上でインタラクティブに確認できる）
fig.show()