
from flask import Flask, render_template,request
import datetime
import board
import time
from functions import *
import requests

app = Flask(__name__)

@app.route('/')
def index():
    ledRedSts = GPIO.input(ledRed)
    ledBluSts = GPIO.input(ledBlue)
    ledGreenSts = GPIO.input(ledGreen)
    temperature,humidity = temperature_humidity()
    templateData = {
        'ledRed' : ledRedSts,
        'ledBlue' : ledBluSts,
        'ledGreen' : ledGreenSts,
        'temperature': temperature,
        'humidity' : humidity
    }
    return render_template('index.html', **templateData)

@app.route('/<deviceName>/<action>')
def action(deviceName,action):
    actuator = 0
    if deviceName == "ledRed":
        actuator = ledRed
    if deviceName == "ledBlue":
        actuator = ledBlue
    if deviceName == "ledGreen":
        actuator = ledGreen
    if deviceName == "ventilator" and action == "on":
        pornireVentilator()
    if deviceName == "ventilator" and action == "off":
        oprireVentilator()
    
    if action == "on" and actuator !=0:
        GPIO.output(actuator,1)
    if action == "off" and actuator !=0:
        GPIO.output(actuator,0)

    ledRedSts = GPIO.input(ledRed)
    ledBluSts = GPIO.input(ledBlue)
    ledGreenSts = GPIO.input(ledGreen)
    temperature,humidity = temperature_humidity()
    templateData = {
              'ledBlue'  : ledBluSts,
              'ledRed'  : ledRedSts,
              'ledGreen': ledGreenSts,
              'temperature': temperature,
              'humidity' : humidity

    }
    return render_template('index.html', **templateData)

@app.route('/temperature', methods=['POST'])
def temperature():
    city = request.form['city']
    r = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=e6af9690fe007c4672bf84ae5f114c9a")
    json_obj = r.json()
    temp_k = float(json_obj['main']['temp'])
    temp_celsius =round(temp_k - 273.15,1)
    ledRedSts = GPIO.input(ledRed)
    ledBluSts = GPIO.input(ledBlue)
    ledGreenSts = GPIO.input(ledGreen)
    temperature,humidity = temperature_humidity()
    templateData = {
              'ledBlue'  : ledBluSts,
              'ledRed'  : ledRedSts,
              'ledGreen': ledGreenSts,
              'temperature': temperature,
              'humidity' : humidity,
              'city' : city,
              'temp' : temp_celsius
    }
    return render_template('temperature.html',**templateData)

@app.route('/alarma',methods=['POST'])
def alarma():
    if request.method == 'POST':
        status = request.form.get('radioButton')
        status_int= int(status)
        ledRedSts = GPIO.input(ledRed)
        ledBluSts = GPIO.input(ledBlue)
        ledGreenSts = GPIO.input(ledGreen)
        temperature,humidity = temperature_humidity()
        senzor_alarma(status_int)
        templateData = {
              'ledBlue'  : ledBluSts,
              'ledRed'  : ledRedSts,
              'ledGreen': ledGreenSts,
              'temperature': temperature,
              'humidity' : humidity,
              'stats' : status_int
            
         }
        return render_template('index.html', **templateData)
    else:
        ledRedSts = GPIO.input(ledRed)
        ledBluSts = GPIO.input(ledBlue)
        ledGreenSts = GPIO.input(ledGreen)
        temperature,humidity = temperature_humidity()
        templateData = {
              'ledBlue'  : ledBluSts,
              'ledRed'  : ledRedSts,
              'ledGreen': ledGreenSts,
              'temperature': temperature,
              'humidity' : humidity
         }
        return render_template('index.html', **templateData)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)