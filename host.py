import socketio
import pyautogui
import base64
import io
from time import sleep
import threading
import os
import serial

# Connect to the Node.js server
sio = socketio.Client()
sio.connect('http://localhost:3000')

clint = ''
pc = ''
user = 'UltronPC'
password = '1'

enable_move = True
enable_click = True
enable_keyboard = True
current_fps = 1 

fps = lambda fps: 1/60 if fps > 60 else (1 if fps < 1 else 1/fps)



serialPort = serial.Serial(
    port='COM8', baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
)


def clear_screen():
    """
    Clears the screen based on the operating system.
    """
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux and macOS
        os.system('clear')

# Removed handle_input function and input_thread

@sio.event
def connect():
    print("Connected to the server")

@sio.event
def disconnect():
    print("Disconnected from the server")

@sio.on('control_id')
def on_control_id(data):
    global pc
    pc = data

    sio.emit('host_info', [pc, user])

@sio.on('host')
def on_host(data):
    global clint
    global password

    if data['password'] == password and clint == '':
        clint = data['clint']
        width, height = pyautogui.size()
        sio.emit('screen_size', {'width': width, 'height': height, 'to': clint})
        print(f'CLINT: {width}x{height} {clint}')

@sio.on('clint_left')
def on_clint_left(data):
    global clint
    if data == clint:
        print(f'CLINT {clint} LEFT')
        clint = ''

@sio.on('remote_control')
def on_remote_control(data):
    global password
    
    control_type = data['type']
    Password = data['password']

    if Password == password and clint == data['me']:
        if control_type == 'mouse_move' and enable_move:
            x, y = data['x'], data['y']
            pyautogui.moveTo(x, y)
        elif control_type == 'mouse_click' and enable_click:
            x, y = data['x'], data['y']
            button = data['button']
            if button == 'left':
                serialPort.write(b"klik\r\n")
            elif button == 'right':
                serialPort.write(b"krik\r\n")
        elif control_type == 'keypress' and enable_keyboard:
            key = data['key']
            print(key)
            if len(key) == 1:
                serialPort.write(f"write {key}\r\n".encode('utf-8'))
            if key == 'Enter':
                serialPort.write(b"enter\r\n")
            if key == 'Backspace':
                serialPort.write(b"backspace\r\n")
            if key == 'Escape':
                serialPort.write(b"escape\r\n")
            # pyautogui.press(key)

def capture_screen():    
    while True:
        # Only capture screen if a client is connected
        if clint:
            # Capture the screen
            screen = pyautogui.screenshot()
            img_bytes = io.BytesIO()
            screen.save(img_bytes, format='JPEG')
            
            # Encode the image as base64
            img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
            
            # Emit the screen data to the server
            sio.emit('screen_share', {'image': img_data, "to": clint})
            
            # Sleep for a bit to control the refresh rate
            sleep(fps(current_fps))
        else:
            # No client connected, sleep longer to reduce CPU usage
            sleep(1)

if __name__ == '__main__':
    try:
        screen_thread = threading.Thread(target=capture_screen)
        
        screen_thread.start()
        
        screen_thread.join()
    except KeyboardInterrupt:
        print("Screen sharing stopped.")
