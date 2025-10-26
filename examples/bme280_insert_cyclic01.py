#モジュールをインポート
import bme280mod       #BME280センサ関連を取扱う
import time            #時間を取扱う
import datetime        #日付と時刻を取扱う
import pymysql.cursors #PythonからDBを取扱う


#このノードを識別するID
NODE_IDENTIFIER = 'tochigi_iot_999'

#DBへの接続情報
DB_USER = 'iot_user'
DB_PASS = 'password'
DB_HOST = 'localhost'
DB_NAME = 'iot_storage'

def main():
    #モジュール内に定義されているメソッドを呼び出す
    bme280mod.init() #BME280センサを初期化

    #DBサーバに接続する
    sql_connection = pymysql.connect(
        user= DB_USER,    #データベースにログインするユーザ名
        passwd = DB_PASS, #データベースユーザのパスワード
        host = DB_HOST,   #接続先DBのホストorIPアドレス
        db = DB_NAME
    )

    print("Database connection established!");
    
    while True:
        bme280mod.read_data()       #測定
        data = bme280mod.get_data() #データを取得

        #ディクショナリからデータを取得
        new_temp = round(data['temperature'], 2) #小数点以下2桁で丸め
        new_hum = round(data['humidity'], 2)
        new_press = round(data['pressure'], 2)
        new_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #DBに渡すための新しいディクショナリ形式にまとめる。
        new_row = {
            "timestamp" : new_timestamp,
            "identifier" : NODE_IDENTIFIER,
            "temperature" : new_temp,
            "humidity" : new_hum,
            "pressure" : new_press
        };

        print(f'●NEW_DATA● TIMESTAMP: {new_timestamp}, TEMP: {new_temp:.2f}, HUMIDITY: {new_hum:.2f}, PRESSURE: {new_press:.2f}')

        #データベースの操作を行う------
        #cursorオブジェクトのインスタンスを生成
        sql_cursor = sql_connection.cursor()
        print('-- クエリの実行(データの挿入)')

        #クエリを指定する。実データは後から指定する。
        query1 = "INSERT INTO Ambient(timestamp, identifier, temperature, humidity, pressure) " \
                " VALUES(%(timestamp)s, %(identifier)s, %(temperature)s, %(humidity)s, %(pressure)s)";

        #クエリを実行する
        result1 = sql_cursor.execute(query1, new_row)
        print('実行するクエリ: ' + query1)
        #クエリを実行した。変更したrowの数が戻り値となる
        print('クエリを実行しました。('+ str(result1) +' row affected.)')

        #変更を実際に反映させる
        sql_connection.commit()

        time.sleep(10)
        
if __name__ == '__main__':
    main()