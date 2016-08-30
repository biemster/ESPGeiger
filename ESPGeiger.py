from machine import Pin, PWM
import time

cumulative_count = 0

def init(pwm_pin = 13, pwm_freq = 10000, pwm_duty = 40, event_pin = 5):
    # PWM for 400V driver (pin13=D7)
    print('HV pin %d, freq %dkHz, duty %d, event pin %d' % (pwm_pin, pwm_freq/1000, pwm_duty, event_pin))
    pwm = PWM(Pin(pwm_pin), freq=pwm_freq, duty=pwm_duty)

    # geiger discharge irq handler (pin5=D1)
    discharge = Pin(event_pin, Pin.IN)
    discharge.irq(trigger=Pin.IRQ_FALLING, handler=geiger_discharge_handler)

def calibrate(duty_start = 10, duty_end = 66, duty_step = 3, t_step = 10):
    steps = len(range(duty_start, duty_end, duty_step))
    if t_step < 1: t_step = 1
    print('Calibrating HV in %d steps of %d seconds (%ds total) from duty=%d to duty=%d' % (steps, t_step, steps*t_step, duty_start, duty_end))
    for d in range(duty_start, duty_end, duty_step):
        cumulative_count = 0
        init(pwm_duty = d)
        time.sleep(t_step) # NOTE: will this work, or does the whole ESP now sleep (and not register counts?)
        print('With PWM duty %d we had %d counts per second' % (d, cumulative_count / t_step))

def geiger_discharge_handler():
    # this handler is called everytime the tube discharges
    cumulative_count += 1
    buzz()

def buzz(buzz_pin = 14):
    # beep buzzer using pwm (pin14=D5)
    # we can't set a frequency, because freq is shared between all PWM's
    beep = PWM(Pin(buzz_pin))
    beep.duty(90)
    time.sleep_ms(7) # NOTE: does this pause the PWM too?
    beep.duty(0)
