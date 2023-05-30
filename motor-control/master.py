import RPi.GPIO as GPIO 
from gpiozero import AngularServo         
from time import sleep
import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

for device in devices:
	print(device.path, device.name, device.phys)
x = int(input("enter event number: "))
device = evdev.InputDevice(f'/dev/input/event{x}')
print(device)
plot = []
def start(plot):
    x= int(input("Insert width of plot:"))
    y= int(input("Insert length of plot:"))
    for i in range(y):
        plot.append([])
        for j in range(x):
            plot[i].append(" ")
            #print(plot)
    GPIO.cleanup()
    ena = 23
    in1 = 24
    in2 = 25
    in3 = 27
    in4 = 22
    enb = 17
    temp1=1
    servoPIN = 16 #plow servo
    servo = AngularServo(servoPIN, min_pulse_width = 0.0006, max_pulse_width = 0.0024)
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

    position = [y-1, x-1]
    position_map = plot
    position_map[position[0]][position[1]] = "x"
    previous_command = ""
    traveled_places = set()
    while(1):
        position_map = position_map
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if "up" in str(evdev.categorize(event)) :
                    print("stop")
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.LOW)

                    GPIO.output(in3, GPIO.LOW)
                    GPIO.output(in4, GPIO.LOW)
                    if previous_command == "up":
                        if f"{position[0]-1}, {position[1]}" in traveled_places:
                            servo.angle = -90
                            print("Servo up")
                        else:
                            servo.angle = 0
                        traveled_places.add(f"{position[0]}, {position[1]}")
                        position_map[position[0]][position[1]] = ' '
                        previous_command = ""
                        position[0] -= 1
                        position_map[position[0]][position[1]] = 'x'
                        for i in range(len(position_map)):
                            print(position_map[i])
                        print()

                    elif previous_command == 'down':
                        if f"{position[0]+1}, {position[1]}" in traveled_places:
                            servo.angle = -90
                            print("Servo up")
                        else:
                            servo.angle = 0
                        traveled_places.add(f"{position[0]}, {position[1]}")
                        position_map[position[0]][position[1]] = ' '
                        previous_command = ""
                        position[0] += 1
                        position_map[position[0]][position[1]] = 'x'
                        for i in range(len(position_map)):
                            print(position_map[i])
                        print()
                    
                    elif previous_command == 'left':
                        if f"{position[0]}, {position[1]-1}" in traveled_places:
                            servo.angle = -90
                            print("Servo up")
                        else:
                            servo.angle = 0
                        traveled_places.add(f"{position[0]}, {position[1]}")
                        position_map[position[0]][position[1]] = ' '
                        previous_command = ""
                        position[1] -= 1
                        position_map[position[0]][position[1]] = 'x'
                        for i in range(len(position_map)):
                            print(position_map[i])
                        print()
                    
                    elif previous_command == 'right':
                        if f"{position[0]}, {position[1]+1}" in traveled_places:
                            servo.angle = -90
                            print("Servo up")
                        else:
                            servo.angle = 0
                        traveled_places.add(f"{position[0]}, {position[1]}")
                        position_map[position[0]][position[1]] = ' '
                        previous_command = ""
                        position[1] += 1
                        position_map[position[0]][position[1]] = 'x'
                        for i in range(len(position_map)):
                            print(position_map[i])
                        print()                   
                            
                elif "BTN_A" in str(evdev.categorize(event)):
                    print("down")
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.HIGH)

                    GPIO.output(in3, GPIO.LOW)
                    GPIO.output(in4, GPIO.HIGH)
                    previous_command = "down"

                elif "BTN_Y" in str(evdev.categorize(event)):
                    print("up")
                    GPIO.output(in1,GPIO.HIGH)
                    GPIO.output(in2,GPIO.LOW)

                    GPIO.output(in3, GPIO.HIGH)
                    GPIO.output(in4, GPIO.LOW)
                    previous_command = "up"


                elif "BTN_X" in str(evdev.categorize(event)):
                    print("left")
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.HIGH)

                    GPIO.output(in3, GPIO.HIGH)
                    GPIO.output(in4, GPIO.LOW)
                    previous_command = "left"


                elif "BTN_B" in str(evdev.categorize(event)):
                    print("right")
                    GPIO.output(in1,GPIO.HIGH)
                    GPIO.output(in2,GPIO.LOW)

                    GPIO.output(in3, GPIO.LOW)
                    GPIO.output(in4, GPIO.HIGH)
                    previous_command = "right"
start(plot)
