from machine import Pin, PWM
import time

def init(pwm_pin = 13, pwm_freq = 10000, pwm_duty = 66):
    # PWM for 400V driver (pin13=D7)
    pwm = PWM(Pin(pwm_pin), freq=pwm_freq, duty=pwm_duty)

def calibrate(duty_start = 33, duty_end = 66, duty_step = 5, t_step = 10):
    steps = int((duty_end-duty_start) / duty_step)
    print 'Calibrating HV in %d steps of %d seconds (%ds total) from duty=%d to duty=%d' % (steps, t_step, steps*t_step, duty_start, duty_end)

def buzz(buzz_pin = 14):
    # beep buzzer using pwm (pin14=D5)
    # we can't set a frequency, because freq is shared between all PWM's
    beep = PWM(Pin(buzz_pin))
    beep.duty(90); time.sleep_ms(7); beep.duty(0)