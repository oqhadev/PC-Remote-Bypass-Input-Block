import socketio
import pyautogui
import base64
import io
import asyncio
from aiohttp import web
from lib.ibinputsimulator import (
    init_simulator,
    simulate_left_click,
    simulate_right_click,
    simulate_key_down_up,
    SendType,
    VK
)


fps = lambda fps: 1/60 if fps > 60 else (1 if fps < 1 else 1/fps)
current_fps = 1 

sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app= web.Application()
sio.attach(app)

connected_client = None
password_client='asd'

@sio.event
async def connect(sid, environ, auth):
    print(f"Connected to the server: {sid}")
    global connected_client
    connected_client = sid

    screen_size = pyautogui.size()
    await sio.emit('screen_size', {'width': screen_size.width, 'height': screen_size.height}, room=sid)


@sio.event
def disconnect(sid):
    print(f"Disconnected from the server: {sid}")
    global connected_client
    connected_client = None


@sio.on('remote_control')
async def on_remote_control(sid, data):
    loop = asyncio.get_running_loop()
    control_type = data['type']

    if connected_client:
        def blocking_pyautogui_action():
            if control_type == 'mouse_move':
                x, y = data['x'], data['y']
                pyautogui.moveTo(x, y)
        await loop.run_in_executor(None, blocking_pyautogui_action)
        if control_type == 'mouse_click':
            button = data['button']
            if button == 'left':
                simulate_left_click()
            elif button == 'right':
                simulate_right_click()
        if control_type == 'keypress':
            key = data['key']
            if len(key) == 1:
                if data['ctrl'] and key.lower() == 's':
                    simulate_key_down_up(VK.END)
                elif data['ctrl'] and key.lower() == 'r':
                    simulate_key_down_up(VK.HOME)
                else:
                    simulate_key_down_up(ord(key.upper()), shift=key.isupper(), ctrl=data.get('ctrl', False))
            if key == 'Enter':
                simulate_key_down_up(VK.RETURN)
            elif key == 'Backspace':
                simulate_key_down_up(VK.BACK)
            elif key == 'Escape':
                simulate_key_down_up(VK.ESCAPE)

async def capture_screen():

    while True:
            if connected_client:
                screen = pyautogui.screenshot()
                img_bytes = io.BytesIO()
                screen.save(img_bytes, format='JPEG',quality=10)
            
                img_data=base64.b64encode(img_bytes.getvalue()).decode('utf-8')
                    
                await sio.emit('screen_share', {'image': img_data},room=connected_client)

                await asyncio.sleep(fps(current_fps)) # Wait before retrying
            else:
                await asyncio.sleep(1) # Wait before retrying


async def index(request):
    global password_client
    global current_fps
    password = request.query.get('password')
    if not password or password != password_client:
        return web.Response(text="Unauthorized", status=401)

    fps= request.query.get('fps', '1')
    if not fps.isdigit():
        return web.Response(text="Invalid FPS value", status=400)
    current_fps= int(fps) 

    try:
        with open('./public/index.html') as f:
            return web.Response(text=f.read(), content_type='text/html')
    except FileNotFoundError:
            return web.Response(text="index.html not found", status=404)

async def start_background_tasks(app):
    print("Server has started up. Starting background task...")
    sio.start_background_task(capture_screen)

def main():
    print("Starting the server...")

    init_result = init_simulator(SendType.Logitech)
    if init_result >= 0:
        print("Input simulator initialized successfully.")
    else:
        print("Failed to initialize input simulator.")

    app.on_startup.append(start_background_tasks)
    app.router.add_get('/', index)
    app.router.add_static('/', './public')
    web.run_app(app, port=3000)

if __name__ == '__main__':
        main()