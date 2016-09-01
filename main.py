import ESPGeiger as geiger

geiger.init()

def click():
    # click the buzzer
    print('.', end='')

count = 0
while True:
    # check if a new event happened
    if geiger.cumulative_count > count:
        count = geiger.cumulative_count
        click()
