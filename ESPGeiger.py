from machine import Pin, PWM
import utime

cumulative_count = 0

def init(pwm_pin = 13, pwm_freq = 10000, pwm_duty = 66, event_pin = 5):
    # PWM for 400V driver (pin13=D7)
    print('HV pin %d, freq %dkHz, duty %d, event pin %d' % (pwm_pin, pwm_freq/1000, pwm_duty, event_pin))
    pwm = PWM(Pin(pwm_pin), freq=pwm_freq, duty=pwm_duty)

    # geiger discharge irq handler (pin5=D1)
    discharge = Pin(event_pin, Pin.IN)
    discharge.irq(trigger=Pin.IRQ_FALLING, handler=geiger_discharge_handler)

def calibrate(duty_start = 20, duty_end = 91, duty_step = 10, t_step = 10):
    global cumulative_count
    
    steps = len(range(duty_start, duty_end, duty_step))
    if duty_start < 5: duty_start = 5
    if duty_end > 95: duty_end = 95
    if t_step < 1: t_step = 1

    print('Calibrating HV in %d steps of %d seconds (%ds total) from duty=%d to duty=%d' % (steps, t_step, steps*t_step, duty_start, duty_end))
    for d in range(duty_start, duty_end, duty_step):
        cumulative_count = 0
        init(pwm_duty = d)
        utime.sleep(t_step)
        print('With PWM duty %d we had %d counts in %d seconds' % (d, cumulative_count, t_step))

def geiger_discharge_handler(p):
    # this handler is called everytime the tube discharges
    global cumulative_count
    cumulative_count += 1
