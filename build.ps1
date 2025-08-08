# Ensure PyInstaller is installed
pip install pyinstaller

# Run PyInstaller to create a single executable and include necessary data files
pyinstaller --collect-all engineio app.py -y --icon icon.ico

# Rename the executable
Rename-Item -Path "dist/app/app.exe" -NewName "PCRemoteBIB.exe"

# Copy additional files to the dist/app/ directory
Copy-Item -Path "IbInputSimulator.dll" -Destination "dist/app/"
Copy-Item -Path "config.ini" -Destination "dist/app/"
Copy-Item -Path "public" -Recurse -Destination "dist/app/"
