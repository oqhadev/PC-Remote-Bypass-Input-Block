# PC Remote Bypass Input Block

This project implements a simple remote desktop solution using Python, with the ability to bypass GameGuard mouse/keyboard blocks on remote. It allows you to control a remote computer and view its screen.

## Prerequisites

Before running the application, you need to install the Logitech Gaming Software (LGS) extension.

1.  Download `LGS.v9.02.65_x64.exe` from [https://github.com/Chaoses-Ib/IbLogiSoftExt/releases/download/v0.1/LGS.v9.02.65_x64.exe](https://github.com/Chaoses-Ib/IbLogiSoftExt/releases/download/v0.1/LGS.v9.02.65_x64.exe).
2.  Run the downloaded executable to install the software.
3.  Restart your PC.
4.  Do not make any changes to the Logitech Gaming Software after installation.

## Setup and Run

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/Python-Remote-Desktop.git
    cd Python-Remote-Desktop
    ```

2.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**

    ```bash
    python app.py
    ```

    The server will start on `http://localhost:3000`.

## Usage

Once the server is running, open your web browser and navigate to `http://localhost:3000/?password=your_password&fps=your_fps`.

*   Replace `your_password` with the password configured in `app.py` (default is `asd`).
*   Replace `your_fps` with the desired frames per second for screen sharing (e.g., `10` for 10 FPS).

You can then interact with the remote desktop through the web interface.
