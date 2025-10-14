import pymysql.cursors #PythonからDBを利用するためのモジュールを利用

def main():
    #DBサーバに接続する
    sql_connection = pymysql.connect(
        user='iot_user',  #データベースにログインするユーザ名
        passwd='password',#データベースユーザのパスワード
        host='localhost', #接続先DBのホストorIPアドス
        db='practice'
    )
    #cursorオブジェクトのインスタンスを生成
    sql_cursor = sql_connection.cursor()

    #テーブルにデータを挿入する
    print('■データを入力してください')
    new_account_id = input('account_id: ')
    new_first_name = input('first_name: ')
    new_last_name = input('last_name: ')
    new_balance = input('balance: ')
    new_atm_count = input('atm_count: ')

    print('●クエリの実行(データの挿入)')

    query1 = 'INSERT INTO BankAccount(account_id, first_name, last_name, balance, atm_count) ' \
                ' VALUES(%s, %s, %s, %s, %s)';

    print('実行するクエリ: ' + query1)
    
    #クエリを実行。変更したrowの数が戻り値となる
    result1 = sql_cursor.execute(query1, (new_account_id, new_first_name, new_last_name, new_balance, new_atm_count))

    print('クエリを実行しました。('+ str(result1) +' row affected.)')

    #変更を実際に反映させる
    sql_connection.commit()

    #挿入したデータを含めてすべてのデータを表示
    print('●クエリの実行(データの選択)')
    query2 = 'SELECT account_id, first_name, last_name, balance, atm_count FROM BankAccount;' #クエリのコマンド


    print('実行するクエリ: ' + query2)
    result2 = sql_cursor.execute(query2) #クエリを実行。取得した row が戻り値となる

    print('クエリを実行しました。('+ str(result2) +' row affected.)')

    print( 'account_id \t', 'first_name \t', 'last_name \t', 'balance \t ','atm_count') #クエリを実行した結果得られたデータを1行ずつ表示する
    for row in sql_cursor.fetchall():
        print( row[0], ', \t', row[1], ', \t', row[2], ', \t', row[3], ', \t', row[4])
main()
