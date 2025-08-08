import ctypes
import random
import os

DLL_PATH = os.path.join(os.getcwd(), "IbInputSimulator.dll")

try:
    _ib_simulator = ctypes.WinDLL(DLL_PATH)
except OSError as e:
    print(f"Error loading DLL: {e}. Make sure IbInputSimulator.dll is in the specified path.")
    _ib_simulator = None

# Define SendType enum (from the C++ header)
class SendType:
    AnyDriver = 0
    SendInput = 1
    Logitech = 2
    LogitechGHubNew = 6
    Razer = 3
    DD = 4
    MouClassInputInjection = 5

# Define MouseButton enum (from the C++ header)
class MouseButton:
    LeftDown = 0x0002
    LeftUp = 0x0004
    Left = LeftDown | LeftUp
    RightDown = 0x0008
    RightUp = 0x0010
    Right = RightDown | RightUp
    MiddleDown = 0x0020
    MiddleUp = 0x0040
    Middle = MiddleDown | MiddleUp
    XButton1Down = 0x0081 # MOUSEEVENTF_XDOWN | XBUTTON1
    XButton1Up = 0x0101 # MOUSEEVENTF_XUP | XBUTTON1
    XButton1 = XButton1Down | XButton1Up
    XButton2Down = 0x0082 # MOUSEEVENTF_XDOWN | XBUTTON2
    XButton2Up = 0x0102 # MOUSEEVENTF_XUP | XBUTTON2
    XButton2 = XButton2Down | XButton2Up

# Define KeyboardModifiers struct
class KeyboardModifiers(ctypes.Structure):
    _fields_ = [
        ("LCtrl", ctypes.c_uint, 1),
        ("LShift", ctypes.c_uint, 1),
        ("LAlt", ctypes.c_uint, 1),
        ("LWin", ctypes.c_uint, 1),
        ("RCtrl", ctypes.c_uint, 1),
        ("RShift", ctypes.c_uint, 1),
        ("RAlt", ctypes.c_uint, 1),
        ("RWin", ctypes.c_uint, 1),
    ]

# Define Virtual Key Codes (common ones)
class VK:
    RETURN = 0x0D # Enter key
    BACK = 0x08 # Backspace key
    ESCAPE = 0x1B # Escape key
    F1 = 0x70
    F2 = 0x71
    F3 = 0x72
    F4 = 0x73
    CONTROL = 0x11 # Control key
    HOME= 0x24 # Home key
    END = 0x23

# Define function signatures
if _ib_simulator:
    # DLLAPI Send::Error __stdcall IbSendInit(Send::SendType type, Send::InitFlags flags, void* argument);
    _ib_simulator.IbSendInit.argtypes = [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
    _ib_simulator.IbSendInit.restype = ctypes.c_uint32 # Send::Error

    # DLLAPI bool __stdcall IbSendMouseClick(Send::MouseButton button);
    _ib_simulator.IbSendMouseClick.argtypes = [ctypes.c_uint32]
    _ib_simulator.IbSendMouseClick.restype = ctypes.c_bool

    # DLLAPI bool __stdcall IbSendKeybdDownUp(uint16_t vk, Send::KeyboardModifiers modifiers);
    _ib_simulator.IbSendKeybdDownUp.argtypes = [ctypes.c_uint16, KeyboardModifiers]
    _ib_simulator.IbSendKeybdDownUp.restype = ctypes.c_bool

    # DLLAPI void __stdcall IbSendDestroy();
    _ib_simulator.IbSendDestroy.argtypes = []
    _ib_simulator.IbSendDestroy.restype = None

def init_simulator(send_type: int, flags: int = 0, argument: ctypes.c_void_p = None) -> int:
    if _ib_simulator:
        return _ib_simulator.IbSendInit(send_type, flags, argument)
    return -1 # Indicate error if DLL not loaded

def destroy_simulator():
    if _ib_simulator:
        _ib_simulator.IbSendDestroy()

def simulate_mouse_down_up(button: int) -> bool:
    if _ib_simulator:
        return _ib_simulator.IbSendMouseClick(button)
    return False

def simulate_left_click() -> bool:
    if simulate_mouse_down_up(MouseButton.LeftDown):
        import time
        time.sleep(random.uniform(0.01, 0.05))  # Simulate a short delay
        return simulate_mouse_down_up(MouseButton.LeftUp)
    return False

def simulate_right_click() -> bool:
    if simulate_mouse_down_up(MouseButton.RightDown):
        import time
        time.sleep(random.uniform(0.01, 0.05))  # Simulate a short delay
        return simulate_mouse_down_up(MouseButton.RightUp)
    return False

def simulate_key_down_up(vk_code: int, shift: bool=False, ctrl:bool=False) -> bool:
    if _ib_simulator:
        modifiers = KeyboardModifiers() # Create a default, empty modifiers object
        modifiers.LCtrl = 0
        modifiers.LShift = 0
        modifiers.LAlt = 0
        modifiers.LWin = 0
        modifiers.RCtrl = 0
        modifiers.RShift = 0
        modifiers.RAlt = 0
        modifiers.RWin = 0

        if ctrl:
            modifiers.LCtrl = 1
        if shift:
            modifiers.LShift = 1
        result = _ib_simulator.IbSendKeybdDownUp(vk_code, modifiers)
        return result
    return False

