# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashとインラインCSSスタイルを使用して、
# 左側にグレーのサイドバー、右側に黒背景のメインエリアを配置した
# ダッシュボードの基本レイアウトサンプルです。
# Flexboxを活用した2カラムレイアウトやネスト構造による構築を学べます。
# ==============================================================================

# 1. ライブラリ・モジュールの読み込み (インポート)
# Webアプリケーション作成用ライブラリ (Dash)
# - Dash: アプリケーション本体
# - html (Dash HTML Components): HTMLタグやCSSスタイルによる見た目の構築を担当する部品
from dash import Dash, html

# 2. アプリの初期化
# Dashアプリケーションインスタンスの生成
app = Dash()

# 3. ダッシュボードレイアウトの定義 (UI・CSS設計)
# アプリケーション全体のHTML構造を定義（左右2カラム構成の親コンテナ）
app.layout = html.Div([
    # ==========================================
    # 3-1. 【左側】サイドバー（コントロール・メニューエリア）
    # ==========================================
    html.Div([
        # サイドバー上部のメインメニュータイトル
        html.H2("DashBord Menu", style={'color': 'white', 'fontSize': '18px', 'marginBottom': '30px'}),
        
        # コントロールパネル見出し
        html.H3("Control Panel", style={'color': 'white', 'fontSize': '13px'}),
        
        # スイッチ項目ラベル
        html.P("switch Panel", style={'color': 'white', 'textAlign': 'center', 'fontSize': '8px'}),
    ], style={
        "backgroundColor": "blue", 
        "width": "200px",
        'height': '100vh', 
        "padding": "25px 20px",
        "boxSizing": "border-box",
        'overflowY': 'auto',          # サイドバー内が長い場合にスクロール可能にする
    }),
    
    # ==========================================
    # 3-2. 【右側】メインコンテンツエリア
    # ==========================================
    html.Div([
        # メインヘッダ（ダッシュボード全体のタイトル）
        html.H1("DashBord LAYOUT", style={'color': 'black', 'fontSize': '30px', 'fontWeight': 'bold', 'marginBottom': '20px'}),
        
        # --- ① 上段：横並び（Flexbox）で配置する2つのカードエリア ---
        html.Div([
            # 1つ目のカードコンポーネント
            html.Div([
                # カード内見出し
                html.H2("Hello", style={'color': 'red', 'textAlign': 'left', 'fontSize': '24px', 'marginBottom': '15px'}),
                
                # ネストされた内部テキスト要素
                html.Div([
                    html.P("Hi", style={'color': 'yellow', 'textAlign': 'left', 'fontSize': '15px'}),
                ]),
            ], style={
                "backgroundColor": "black",  
                "padding": "10px",
                "borderRadius": "8px",
                "height": "250px",
                "maxWidth": "500px",
                "flex": "1"                 # 柔軟に領域を分割
            }),
            
            # 2つ目のカードコンポーネント
            html.Div([
                # カード内見出し
                html.H2("Hello", style={'color': 'red', 'textAlign': 'center', 'fontSize': '24px', 'marginBottom': '15px'}),
                
                # カード内テキスト要素
                html.P("Hi", style={'color': 'yellow', 'textAlign': 'center', 'fontSize': '15px'}),
            ], style={
                "backgroundColor": "black",  
                "padding": "10px",
                "borderRadius": "8px",
                "height": "250px",
                "maxWidth": "500px",
                "flex": "1"                 # 柔軟に領域を分割
            }),
            
            # 3つ目のカードコンポーネント
            html.Div([
                # カード内見出し
                html.H2("Hello", style={'color': 'red', 'textAlign': 'right', 'fontSize': '24px', 'marginBottom': '15px'}),
                
                # カード内テキスト要素
                html.P("Hi", style={'color': 'yellow', 'textAlign': 'right', 'fontSize': '15px'}),
            ], style={
                "backgroundColor": "black",  
                "padding": "10px",
                "borderRadius": "8px",
                "height": "250px",
                "maxWidth": "500px",
                "flex": "1"                 # 柔軟に領域を分割
            }),
        ], style={
            "display": "flex",              # 子要素を横並びにする
            "gap": "20px",                  # カード間の隙間を設定
            "marginBottom": "20px"
        }),
        
        # --- ② 下段：単体で配置する大きめのカードエリア ---
        html.Div([
            # カード内見出し
            html.H3("Python", style={'color': 'blue', 'textAlign': 'center', 'fontSize': '24px', 'marginBottom': '15px'}),
            
            # カード内テキスト要素
            html.P("Dash", style={'color': 'green', 'textAlign': 'center', 'fontSize': '15px'}),
        ], style={
            "backgroundColor": "black",  
            "padding": "10px",
            "borderRadius": "8px",
            "height": "300px",
        }),
    ], style={
        "flex": "1",                    # 残りの画面幅いっぱいに広げる
        "backgroundColor": "white", 
        "minHeight": "100vh", 
        "padding": "20px",
        "boxSizing": "border-box",
        "overflowY": "auto"             # コンテンツが縦に溢れた場合にスクロール可能にする
    })
], style={
    "display": "flex",                  # 左右のブロックを横並びにする
    "height": "100vh",                  # 画面の高さいっぱいに固定
    "overflow": "hidden",                # 画面全体での不要な二重スクロールを抑制
    "margin": "0"
})

# 4. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動する
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8050, debug=False)