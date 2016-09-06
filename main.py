from machine import Pin
import utime
from umqtt.robust import MQTTClient
import ESPGeiger as geiger

geiger.init()
MQTT_SERVER = "<IP or DNS record>"
MQTT_PORT = 1883
MQTT_USR = None
MQTT_PWD = None
mqtt = MQTTClient("ESPGeiger", MQTT_SERVER, port=MQTT_PORT, user=MQTT_USR, password=MQTT_PWD)
mqtt.connect()

# buzzer is between pin14=D5 and pin12=D6
D5 = Pin(14, Pin.OUT)
D6 = Pin(12, Pin.OUT)

def click():
    # click the buzzer connected to pins pin14=D5 and pin12=D6
    D5.high()
    D6.low()
    print('.', end='')
    utime.sleep_ms(2)
    D5.low()
    D6.high()

    # set pins low after click
    utime.sleep_ms(2) # this goes into dead time of the counter
    D6.low()

count = 0
last_tick = utime.ticks_ms()
curr_tick = utime.ticks_ms()
CPMlist = list()
while True:
    # check if a new event happened
    if geiger.cumulative_count > count:
        count = geiger.cumulative_count
        curr_tick = utime.ticks_ms()
        delta_t = utime.ticks_diff(last_tick, curr_tick)
        last_tick = curr_tick

        if delta_t < 120000:
            CPMlist.append(delta_t)
            while sum(CPMlist) > 60000: CPMlist.pop(0)
        
        click()
        msg = b'(' + bytes(str(len(CPMlist)), 'ascii') + b',' + bytes(str(delta_t), 'ascii') + b')'
        mqtt.publish(topic=b"ESPGeiger tick", msg=msg)
