import board
import digitalio
import analogio
import dht11
import time
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT




t = 0
buttonval = False
processtimeT = 0
processtimeB = 0
processtimeP = 0
processtimeU = 0
scheduler_delay = 0.001
aio_username = "kenozzz"
aio_key = 'aio_WKDS322KVTkyWxM6xUCNvBtn9Ela'
ssid = 'iphone'
pwd = '12345678'
print("Connecting to %s" % ssid)
wifi.radio.connect(ssid, pwd)
print("Connected to %s!" % ssid)
pool = socketpool.SocketPool(wifi.radio)
mqtt_client = MQTT.MQTT(
    broker = 'io.adafruit.com',
    port = 1883,
    username = aio_username,
    password = aio_key,
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)
mqtt_client.connect()

th = dht11.DHT11(board.GP2)
button = digitalio.DigitalInOut(board.GP1)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
    

def uplink():
    global processtimeU
    processtimeU = time.monotonic()
    mqtt_client.publish(topic='kenozzz/feeds/temperature', msg=str(t))
    print('Uploaded temperature')
    processtimeU = time.monotonic() - processtimeU
    time.sleep(2)
    
def readtemp():
    global t
    global h
    global processtimeT
    processtimeT = time.monotonic()
    try:
        t = th.temperature
    except RuntimeError:
        print('dht11 err')
    print(t)
    processtimeT = time.monotonic() - processtimeT

def checkbutton():
    global buttonval
    global processtimeB
    processtimeB = time.monotonic()
    buttonval = button.value
    processtimeB = time.monotonic() - processtimeB
    time.sleep(0.1)

def printtest():
    processtimeP = time.monotonic()
    if buttonval:
        processtimeP = time.monotonic() - processtimeP
    else:
        processtimeP = time.monotonic() - processtimeP
        print(f'Process time for print: {processtimeP} seconds\n'+
              f'Process time for temp: {processtimeT} seconds\n'+
              f'Process time for button: {processtimeB} seconds\n'+
              f'Process time for uplink: {processtimeU} seconds\n')

def main():
    readtemp()
    uplink()
    checkbutton()
    printtest()
while True:
    main()
    
    
    
    


