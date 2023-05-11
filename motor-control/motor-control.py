import RPi.GPIO as GPIO          
from time import sleep
import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

for device in devices:
	print(device.path, device.name, device.phys)
x = int(input("enter event number: "))
device = evdev.InputDevice(f'/dev/input/event{x}')
print(device)

if __name__ == "__main__":
    GPIO.cleanup()
    ena = 26
    in1 = 5
    in2 = 6
    in3 = 27
    in4 = 22
    enb = 17
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
    p.start(75) #25 = low, 50 = medium, 75 = high
    q.start(75)

    print("Reading all inputs from gamepad 0")
    print("stop")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)

    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    while(1):
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if "up" in str(evdev.categorize(event)) :
                    print("stop")
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.LOW)

                    GPIO.output(in3, GPIO.LOW)
                    GPIO.output(in4, GPIO.LOW)
                elif "BTN_A" in str(evdev.categorize(event)):
                    print("down")
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.HIGH)

                    GPIO.output(in3, GPIO.LOW)
                    GPIO.output(in4, GPIO.HIGH)

                elif "BTN_Y" in str(evdev.categorize(event)):
                    print("up")
                    GPIO.output(in1,GPIO.HIGH)
                    GPIO.output(in2,GPIO.LOW)

                    GPIO.output(in3, GPIO.HIGH)
                    GPIO.output(in4, GPIO.LOW)

                elif "BTN_X" in str(evdev.categorize(event)):
                    print("left")
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.HIGH)

                    GPIO.output(in3, GPIO.HIGH)
                    GPIO.output(in4, GPIO.LOW)

                elif "BTN_B" in str(evdev.categorize(event)):
                    print("right")
                    GPIO.output(in1,GPIO.HIGH)
                    GPIO.output(in2,GPIO.LOW)

                    GPIO.output(in3, GPIO.LOW)
                    GPIO.output(in4, GPIO.HIGH)
