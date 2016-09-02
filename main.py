from machine import Pin
import utime
import ESPGeiger as geiger

geiger.init()

# buzzer is between pin14=D5 and pin12=D6
D5 = Pin(14, Pin.OUT)
D6 = Pin(12, Pin.OUT)

def click():
    # click the buzzer connected to pins pin14=D5 and pin12=D6
    global D5, D6
    D5.high()
    D6.low()
    print('.', end='')
    utime.sleep_ms(2) # use 4 or 5 to get a lower tone
    D5.low()
    D6.high()

    # set pins low after click
    utime.sleep_ms(2) # this goes into dead time of the counter
    D6.low()

count = 0
while True:
    # check if a new event happened
    if geiger.cumulative_count > count:
        count = geiger.cumulative_count
        click()
