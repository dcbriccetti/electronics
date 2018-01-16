from bottle import route, run, template, request
import RPi.GPIO as GPIO
import time
from random import choice

GPIO.setmode(GPIO.BCM)
RED, GREEN, BLUE = 18, 24, 23
ALL = (RED, GREEN, BLUE)
GPIO.setup(ALL, GPIO.OUT)


@route('/')
def index():
	return template('home.tpl')
	
@route('/on')
def index():
	GPIO.output(RED, 1)
	return template('home.tpl')


@route('/off')
def index():
	GPIO.output(RED, 0)
	return template('home.tpl')
	
@route('/blinkblue')
def index():
    for b in range(4):
        GPIO.output(BLUE, 1)
        time.sleep(.5)
        GPIO.output(BLUE, 0)
        time.sleep(.5)
    return template('home.tpl')

@route('/blinkboth')
def index():
    for b in range(3):
        GPIO.output(BLUE, 1)
        time.sleep(.5)
        GPIO.output(BLUE, 0)
        GPIO.output(RED, 1)
        time.sleep(.5)
        GPIO.output(RED, 0)
    return template('home.tpl')
    
@route('/blinktogether')
def index():
    for b in range(3):
        GPIO.output(BLUE, 1)
        GPIO.output(RED, 1)
        time.sleep(.5)
        GPIO.output(BLUE, 0)
        GPIO.output(RED, 0)
        time.sleep(.5)
    return template('home.tpl')

@route('/blinkall')
def index():
    for b in range(10):
        for color in (GREEN, BLUE, RED):
            for power_state in (1, 0):
                GPIO.output(color, power_state)
                time.sleep(.05)
    return template('home.tpl')    

combos = (
    (RED, ),
    (GREEN, ),
    (BLUE, ),
    (RED, GREEN, BLUE),
    (RED, BLUE),
    (RED, GREEN),
    (BLUE, GREEN)
    )
    
@route('/show7')
def index():
    for combo in combos:
        show_combo(combo, .2)
    return template('home.tpl')    

@route('/random')
def index():
    for n in range(8):
        show_combo(choice(combos), 2)
    return template('home.tpl')

@route('/snazzyblink')
def index():
    for g in range(100):
        GPIO.output(GREEN, 1)
        time.sleep(.001)
        GPIO.output(GREEN, 0)
        time.sleep(.001)
    return template('home.tpl')


def show_combo(combo, time_shown_seconds):
    GPIO.output(combo, 1)
    time.sleep(time_shown_seconds)
    GPIO.output(combo, 0)

try:
    run(host='0.0.0.0', port=8080)
finally:
    GPIO.cleanup()
	
