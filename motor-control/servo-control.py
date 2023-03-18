from gpiozero import AngularServo
from time import sleep


if __name__ == "__main__":
    servoPIN = 17
    servo = AngularServo(servoPIN, min_pulse_width = 0.0006, max_pulse_width = 0.0024)

    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    for device in devices:
        print(device.path, device.name, device.phys)
    x = int(input("enter event number: "))
    device = evdev.InputDevice(f'/dev/input/event{x}')
    print(device)
    while True:
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if "up" in str(evdev.categorize(event)) :
                    print("neutral")
                    servo.angle = 0
                    sleep(1)
                elif "BTN_A" in str(evdev.categorize(event)):
                    print("-90")
                    servo.angle = -90
                    sleep(1)
                elif "BTN_Y" in str(evdev.categorize(event)):
                    print("90")
                    servo.angle = 90
                    sleep(1)
        
