import RPi.GPIO as GPIO          
from time import sleep
from pyjoycon import JoyCon, get_R_id

joycon_id = get_R_id()
joycon = JoyCon(*joycon_id)

joycon.get_status()

in1 = 2
in2 = 3
in3 = 4
in4 = 5
ena = 0
enb = 6
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p=GPIO.PWM(ena,1000)
q=GPIO.PWM(enb,1000)
p.start(25) #25 = low, 50 = medium, 75 = high
q.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

while(1):
    if joycon.get_status()['analog-sticks']['right']['vertical'] == 1644 and joycon.get_status()['analog-sticks']['right']['horizontal'] == 2170:
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)

        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)
    elif joycon.get_status()['analog-sticks']['right']['vertical'] < 900:
        print("down")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)

        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)

    elif joycon.get_status()['analog-sticks']['right']['vertical'] > 2000:
        print("up")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)

        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)

    elif joycon.get_status()['analog-sticks']['right']['horizontal'] < 900:
        print("left")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)

        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)

    elif joycon.get_status()['analog-sticks']['right']['horizontal'] > 2000:
        print("right")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)

        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)
