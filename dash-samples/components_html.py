# ==============================================================================
# 【プログラム概要】
# このスクリプトは、DashのHTMLコンポーネント（html.Div, html.H1〜H6, html.P）を使用して、
# Webブラウザ上に各種見出しタグや段落テキストといった基本的なHTML要素を
# 表示・確認するための最もシンプルなDash Webアプリケーションです。
# ==============================================================================

# 1. ライブラリ・モジュールの読み込み (インポート)
# Webアプリケーション作成用ライブラリ (Dash)
# - Dash: アプリケーション本体を作成
# - html (Dash HTML Components): HTMLの見た目（見出しや枠組みなど）を作る部品
from dash import Dash, html

# 2. アプリの初期化
# アプリの初期化（Dashのインスタンス生成）
app = Dash()

# 3. ダッシュボードのレイアウト定義 (UI設計)
# 画面上に配置するHTML要素（H1〜H6の見出しや、Pタグによる段落）を組み立てます
app.layout = html.Div([
    # 各種見出しタグ (<h1> 〜 <h6> に相当)
    html.H1("Hello Dash"),
    html.H2("Hello Dash"),
    html.H3("Hello Dash"),
    html.H4("Hello Dash"),
    html.H5("Hello Dash"),
    html.H6("Hello Dash"),
    
    # 複数行の段落をまとめるDivコンテナ
    # ※ 複数の子要素を渡すため、リスト [...] で囲んでいます
    html.Div([
        html.P("Hello Python"),
        html.P("Hello Python")
    ])
])

# 4. アプリケーションの実行
# スクリプトが直接実行された場合にのみWebサーバを起動
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8050, debug=False)