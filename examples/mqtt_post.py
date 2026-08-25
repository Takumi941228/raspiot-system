#PahoのMQTTライブラリを使用する
import paho.mqtt.client as mqtt
import json

MQTT_HOST = '10.45.45.21'
MQTT_PORT = 1883
MQTT_TOPIC = 'esp32/mode'

def connect():
  global mqttClient
  mqttClient = mqtt.Client()

  #MQTTブローカーに接続する
  mqttClient.connect(MQTT_HOST, MQTT_PORT, 120)

  #データを送信を開始する
  mqttClient.loop_start()

connect()

print(' <<Mode Mune>> ')
print(' 0:Red LED ')
print(' 1:Green LED ')
print(' 2:Yellow LED ')
print(' q:Exit ')

try:
  while True:
    num = input(' Set Number: ')

    if num == 'q':
      print("Exit!")
      break;
    if num in ['0', '1', '2']:
      num = int(num)

      payload = json.dumps({"mode": num})

      mqttClient.publish(MQTT_TOPIC, payload, qos=0)
    else:
      print(' Invalid Value!! ')

finally:
  mqttClient.loop_stop()
  mqttClient.disconnect()      
