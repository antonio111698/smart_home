import RPi.GPIO as GPIO
import datetime
import dht11
import board
import time
import smtplib, pigpio

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Declararea pinilor pentru ventilator
motorspeed_pin = 15
DIRA = 18
DIRB = 12

delayOn = 3
delayOff = 1.5

ledRed = 26
ledBlue = 19
ledGreen = 13
#Declararea pinilor pentru senzorul ultrasonic
trig =21
echo = 20
instance = dht11.DHT11(pin = 25)

redLedStatus = 0
blueLedStatus = 0
greenLedStatus =0
temperature = 0
humidity = 0

#Inițializare LED-uri
GPIO.setup(ledRed,GPIO.OUT)
GPIO.setup(ledBlue,GPIO.OUT)
GPIO.setup(ledGreen,GPIO.OUT)
#Inițializare senzor ultrasonic
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

#Inițializare pini ventilator
GPIO.setup(motorspeed_pin,GPIO.OUT)
GPIO.setup(DIRA,GPIO.OUT)
GPIO.setup(DIRB,GPIO.OUT)
#Inițializare motor
pwmPIN =GPIO.PWM(motorspeed_pin,100)
pwmPIN.start(0)

#Led-uri stinse la pornirea sistemului
GPIO.output(ledRed,0)
GPIO.output(ledBlue,0)
GPIO.output(ledGreen,0)

server=smtplib.SMTP('smtp.gmail.com',587) 
server.starttls()
server.login("raspberrypi8989@gmail.com","Student123?")
msg="A fost detectata miscare "

def oprireVentilator():
    pwmPIN.ChangeDutyCycle(0)
    GPIO.output(DIRA,0)
    GPIO.output(DIRB,0)
    time.sleep(delayOff)
def pornireVentilator():
    pwmPIN.ChangeDutyCycle(100)
    GPIO.output(DIRA,1)
    GPIO.output(DIRB,0)


def temperature_humidity(): 
    while True:
        result = instance.read()
        if result.is_valid():
            break
    return result.temperature, result.humidity

def calculate_distance():
    #set the trigger to HIGH
    GPIO.output(trig, GPIO.HIGH)

    #sleep 0.00001 s and the set the trigger to LOW
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)

    #save the start and stop times
    start = time.time()
    stop = time.time()

    #modify the start time to be the last time until
    #the echo becomes HIGH
    while GPIO.input(echo) == 0:
        start = time.time()

    #modify the stop time to be the last time until
    #the echo becomes LOW
    while  GPIO.input(echo) == 1:
        stop = time.time()

    #get the duration of the echo pin as HIGH
    duration = stop - start

    #calculate the distance
    distance = 34300/2 * duration

    if distance < 0.5 and distance > 4000:
        return 0
    else:
        #return the distance
        return int(distance)

def senzor_alarma(status_alarma):
    pi = pigpio.pi()
    buzzer = 7
    pi.set_mode(buzzer, pigpio.OUTPUT)
    while status_alarma == 1:
        if calculate_distance() < 25:
            print(calculate_distance())
            pi.set_PWM_dutycycle(buzzer,200)
            time.sleep(2)
            server.sendmail("raspberrypi8989@gmail.com","antonio_artimon@yahoo.com",msg)
            pi.set_PWM_dutycycle(buzzer,0)
            time.sleep(2.5)
        else:
            pass
    pi.write(buzzer,0)
    pi.stop()

