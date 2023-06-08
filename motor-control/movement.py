import RPi.GPIO as GPIO 
from gpiozero import AngularServo         
import time
from datetime import datetime, timedelta
import click
from colorama import Fore
from colorama import init as colorama_init
from art import text2art
from tqdm import trange

colorama_init(autoreset=True)

@click.command()
def makeCLI():
    click.clear()
    title = text2art("SNOWMERDINGER", font='medium')
    print(f"{Fore.LIGHTCYAN_EX}{title}")
    click.pause()
    click.clear()
    artl4 = text2art("MENU", font='medium')
    print(f"{Fore.LIGHTCYAN_EX}{artl4}")
    width = click.prompt(
        'Enter the width of the plot in meters ', type=int, default=1)
    height = click.prompt('Enter the height of the plot in meters ', type=int, default=1)
    if width <= 0:
        width = 1
    if height <=0:
        height = 1
    artl5 = "Place your robot at the bottom right corner of the plot and press any key to start"
    print(f"{Fore.LIGHTRED_EX}{artl5}")
    click.pause()
    click.clear()
    GPIO.cleanup()
    ena = 23
    in1 = 24
    in2 = 25
    in3 = 27
    in4 = 22
    enb = 17
    temp1=1
    servoPIN = 16
    servo2PIN = 6
    servo = AngularServo(servoPIN, min_pulse_width = 0.0006, max_pulse_width = 0.0024)
    servo2 = AngularServo(servo2PIN, min_pulse_width = 0.0006, max_pulse_width = 0.0024)
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
    p.start(75) #25 = low, 50 = medium, 75 = high
    q.start(75)

    print("Reading all inputs from gamepad 0")
    print("stop")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)

    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

    forward_time = 5 * height/2
    turn_time = 1 
    shift_time = 1 * width/2
    iterations = 9

    servo.angle = 10
    servo2.angle = -90
    for i in range(iterations):
        t_end = time.time() + forward_time
        while time.time() < t_end:
            print("move")
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)

            GPIO.output(in3, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)
        t_end = time.time() + turn_time

        if i != iterations-1:
            while time.time() < t_end: 
                print("turn")
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)

                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)
            t_end = time.time() + shift_time
            while time.time() < t_end:
                print("shift")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)

                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)
            t_end = time.time() + turn_time
            while time.time() < t_end: 
                print("turn")
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)

                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)
        else:
            servo.angle = 90
            t_end = time.time() + 2*turn_time        
            while time.time() < t_end: 
                print("turn")
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)

                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)
            
            t_end = time.time() + forward_time
            while time.time() < t_end:
                print("move")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)

                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)
             
            t_end = time.time() + turn_time        
            while time.time() < t_end: 
                print("turn")
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)

                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)

            t_end = time.time() + forward_time
            while time.time() < t_end:
                print("move")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)

                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)

if __name__ == "__main__":

    makeCLI()
