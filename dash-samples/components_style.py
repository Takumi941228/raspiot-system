# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashとインラインCSSスタイルを使用して、
# 黒背景の全画面（ビューポート）の中央に黄色い背景のコンテンツブロックを配置し、
# その中に赤色の見出しと青色の段落テキストをスタイリング付きで美しくレイアウトした
# 最も基本的なWebアプリケーションのデザインサンプルです。
# Flexboxを活用した要素の中央寄せ配置や、ネスト（入れ子）構造によるレイアウト構築を学べます。
# ==============================================================================

# 1. ライブラリ・モジュールの読み込み (インポート)
# Webアプリケーション作成用ライブラリ (Dash)
# - Dash: アプリケーション本体を作成
# - html (Dash HTML Components): HTMLタグやCSSスタイルによる見た目の構築を担当する部品
from dash import Dash, html

# 2. アプリの初期化
# アプリの初期化（Dashのインスタンス生成）
app = Dash()

# 3. ダッシュボードレイアウトの定義 (UI・CSS設計)
# 黒背景の全画面（ビューポート）の中に、黄色い背景のコンテンツブロックを配置し、
# その中に赤色の見出しと青色の段落テキストをスタイリング付きで配置します。
app.layout = html.Div(
    [
        # 【内側コンテナ】黄色い背景を持つボックス領域
        html.Div(
            [
                # 【見出し】赤色・中央揃え・フォントサイズ30pxの <h1> タグ
                html.H1("Hello Dash", style={"color": "red", "textAlign": "center", "fontSize": 30}),
                
                # 【テキスト用ラッパー】段落を囲むDivブロック
                html.Div(
                    [
                        # 【段落テキスト】青色・中央揃え・フォントサイズ15pxの <p> タグ
                        html.P("Hello Python", style={"color": "blue", "textAlign": "center", "fontSize": 15})
                    ]
                ),
            ],
            style={"backgroundColor": "yellow", "padding": "20px", "borderRadius": "8px"}
        ),
    ],
    # 【外側コンテナ（ベース画面）】画面全体（黒背景、幅100vw、高さ100vh）のレイアウト設定
    style={
        "backgroundColor": "black", 
        "width": "100vw", 
        "height": "100vh", 
        "padding": "20px",
        "boxSizing": "border-box",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center"
    },
)

# 4. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(debug=False)