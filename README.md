# PC Remote Bypass Input Block

This project implements a simple remote desktop solution using Python, with the ability to bypass GameGuard mouse/keyboard blocks on remote. It allows you to control a remote computer and view its screen.

## Configuration

The application's password and port are configured in `config.ini`.

```ini
[SERVER]
password = yourpassword
port = 3000
```

You can modify these values to suit your needs.

## Prerequisites

Before running the application, you need to install the Logitech Gaming Software (LGS) extension.

1.  Download `LGS.v9.02.65_x64.exe` from [https://github.com/Chaoses-Ib/IbLogiSoftExt/releases/download/v0.1/LGS.v9.02.65_x64.exe](https://github.com/Chaoses-Ib/IbLogiSoftExt/releases/download/v0.1/LGS.v9.02.65_x64.exe).
2.  Run the downloaded executable to install the software.
3.  Restart your PC.
4.  Do not make any changes to the Logitech Gaming Software after installation.

## Setup and Run

Download the latest release from [https://github.com/oqhadev/PC-Remote-Bypass-Input-Block/releases](https://github.com/oqhadev/PC-Remote-Bypass-Input-Block/releases).

## Usage

Once the server is running, open your web browser and navigate to `http://localhost:PORT/?password=YOUR_PASSWORD&fps=your_fps`.

- Replace `PORT` with the port configured in `config.ini` (default is `3000`).
- Replace `YOUR_PASSWORD` with the password configured in `config.ini` (default is `yourpassword`).
- Replace `your_fps` with the desired frames per second for screen sharing (e.g., `10` for 10 FPS).

You can then interact with the remote desktop through the web interface.
