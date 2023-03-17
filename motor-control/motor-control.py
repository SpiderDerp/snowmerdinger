#import RPi.GPIO as GPIO          
from time import sleep

from ctypes import WinDLL, WinError, Structure, POINTER, byref, c_ubyte
from ctypes.util import find_library
from ctypes.wintypes import DWORD, WORD, SHORT

BYTE = c_ubyte
# Max number of controllers supported
XUSER_MAX_COUNT = 4

from ctypes import WinDLL, WinError, Structure, POINTER, byref, c_ubyte
from ctypes.util import find_library
from ctypes.wintypes import DWORD, WORD, SHORT
BYTE = c_ubyte
# Max number of controllers supported
XUSER_MAX_COUNT = 4

#gamepad classes and stuff
class XINPUT_BUTTONS(Structure):
    """Bit-fields of XINPUT_GAMEPAD wButtons"""

    _fields_ = [
        ("DPAD_UP", WORD, 1),
        ("DPAD_DOWN", WORD, 1),
        ("DPAD_LEFT", WORD, 1),
        ("DPAD_RIGHT", WORD, 1),
        ("START", WORD, 1),
        ("BACK", WORD, 1),
        ("LEFT_THUMB", WORD, 1),
        ("RIGHT_THUMB", WORD, 1),
        ("LEFT_SHOULDER", WORD, 1),
        ("RIGHT_SHOULDER", WORD, 1),
        ("_reserved_1_", WORD, 1),
        ("_reserved_1_", WORD, 1),
        ("A", WORD, 1),
        ("B", WORD, 1),
        ("X", WORD, 1),
        ("Y", WORD, 1)
    ]
    
    def __repr__(self):
        r = []
        for name, type, size in self._fields_:
            if "reserved" in name:
                continue
            r.append("{}={}".format(name, getattr(self, name)))
        args = ', '.join(r)
        return f"{args}"
    

class XINPUT_GAMEPAD(Structure):
    """Describes the current state of the Xbox 360 Controller.
    
    https://docs.microsoft.com/en-us/windows/win32/api/xinput/ns-xinput-xinput_gamepad
    
    wButtons is a bitfield describing currently pressed buttons
    """
    _fields_ = [
        ("wButtons", XINPUT_BUTTONS),
        ("bLeftTrigger", BYTE),
        ("bRightTrigger", BYTE),
        ("sThumbLX", SHORT),
        ("sThumbLY", SHORT),
        ("sThumbRX", SHORT),
        ("sThumbRY", SHORT),
    ]
    
    def __repr__(self):
        r = []
        r.append(getattr(self, "sThumbRX"))
        r.append(getattr(self, "sThumbRY"))
        args = r
        return f"{args}"


class XINPUT_STATE(Structure):
    """Represents the state of a controller.
    
    https://docs.microsoft.com/en-us/windows/win32/api/xinput/ns-xinput-xinput_state
    
    dwPacketNumber: State packet number. The packet number indicates whether
        there have been any changes in the state of the controller. If the
        dwPacketNumber member is the same in sequentially returned XINPUT_STATE
        structures, the controller state has not changed.
    """
    _fields_ = [
        ("dwPacketNumber", DWORD),
        ("Gamepad", XINPUT_GAMEPAD)
    ]
    
    def __repr__(self):
        return f"XINPUT_STATE(dwPacketNumber={self.dwPacketNumber}, Gamepad={self.Gamepad})"

class XInput:
    """Minimal XInput API wrapper"""

    def __init__(self):
        # https://docs.microsoft.com/en-us/windows/win32/xinput/xinput-versions
        # XInput 1.4 is available only on Windows 8+.
        # Older Windows versions are End Of Life anyway.
        lib_name = "XInput1_4.dll"  
        lib_path = find_library(lib_name)
        if not lib_path:
            raise Exception(f"Couldn't find {lib_name}")
        self._XInput_ = WinDLL(lib_path)
        self._XInput_.XInputGetState.argtypes = [DWORD, POINTER(XINPUT_STATE)]
        self._XInput_.XInputGetState.restype = DWORD

    def GetState(self, dwUserIndex):
        state = XINPUT_STATE()
        ret = self._XInput_.XInputGetState(dwUserIndex, byref(state))
        if ret:
            raise WinError(ret)
        return str(state.Gamepad)


if __name__ == "__main__":
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
    
    xi = XInput()
    from time import sleep
    for x in range(XUSER_MAX_COUNT):
        try:
            print(f"Reading input from controller {x}")
            print(xi.GetState(x))
        except Exception as e:
            print(f"Controller {x} not available: {e}")

    print("Reading all inputs from gamepad 0")
    while True:
        res = xi.GetState(0).strip('][').split(', ')
        if abs(int(res[0])) < 30000 and abs(int(res[1]))  < 30000 :
            print("stop")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)

            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)
        elif int(res[1]) < -30000:
            print("down")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)

            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)

        elif int(res[1]) > 30000:
            print("up")
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)

            GPIO.output(in3, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)

        elif int(res[0]) < -30000:
            print("left")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)

            GPIO.output(in3, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)

        elif int(res[0]) > 30000:
            print("right")
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)

            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)
        sleep(0.016)



  
