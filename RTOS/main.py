import pyRTOS
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

def uplink(self):
    global processtimeU
    aio_username = "kenozzz"
    aio_key = 'aio_WKDS322KVTkyWxM6xUCNvBtn9Ela'
    ssid = 'iphone'
    pwd = '12345678'
    print("Connecting to %s" % ssid)
    wifi.radio.connect(ssid, pwd)
    print("Connected to %s!" % ssid)
    pyRTOS.timeout(0.5)
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
    yield
    while True:
        processtimeU = time.monotonic()
        mqtt_client.publish(topic='kenozzz/feeds/temperature', msg=str(t))
        print('Uploaded temperature')
        processtimeU = time.monotonic() - processtimeU
        yield [pyRTOS.timeout(2)]
        
    
def readtemp(self):
    th = dht11.DHT11(board.GP2)
    global t
    global h
    global processtimeT
    yield
    while True:
        processtimeT = time.monotonic()
        try:
            t = th.temperature
        except RuntimeError:
            continue
        print(t)
        processtimeT = time.monotonic() - processtimeT
        yield [pyRTOS.timeout(2)]

def checkbutton(self):
    global buttonval
    global processtimeB
    button = digitalio.DigitalInOut(board.GP1)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    yield
    while True:
        processtimeB = time.monotonic()
        buttonval = button.value
        processtimeB = time.monotonic() - processtimeB
        yield [pyRTOS.timeout(0.1)]

def printtest(self):
    global processtimeP
    global t
    yield
    while True:
        processtimeP = time.monotonic()
        if buttonval:
            processtimeP = time.monotonic() - processtimeP
        else:
            processtimeP = time.monotonic() - processtimeP
            print(f'Process time for print: {processtimeP}\n'+
                  f'Process time for temp: {processtimeT}\n'+
                  f'Process time for button: {processtimeB}\n'+
                  f'Process time for uplink: {processtimeU}\n')
        yield [pyRTOS.timeout(0.1)]

# Service Routine function
def delay_sr():
	global scheduler_delay
	time.sleep(scheduler_delay)

pyRTOS.add_task(pyRTOS.Task(uplink, priority=1)) 
pyRTOS.add_task(pyRTOS.Task(checkbutton, priority=2))
pyRTOS.add_task(pyRTOS.Task(printtest, priority=3))
pyRTOS.add_task(pyRTOS.Task(readtemp, priority=4)) 

pyRTOS.start()
