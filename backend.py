from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import subprocess
import os
import signal
import sys
import glob
from collections import deque
import threading
import time

app = FastAPI()

# Global variable to keep track of the process and logs
ears_process = None
log_buffer = deque(maxlen=200)  # Store last 200 log lines

class LoginCredentials(BaseModel):
    email: str
    password: str

def read_process_output(process):
    """
    Reads stdout/stderr from the subprocess and appends to log_buffer.
    """
    try:
        if process.stdout:
            for line in iter(process.stdout.readline, ''):
                if line:
                    log_buffer.append(line.strip())
                else:
                    break
    except Exception as e:
        log_buffer.append(f"LOGGING ERROR: {e}")

@app.post("/login")
def login(credentials: LoginCredentials):
    """
    Updates the config.py file with new credentials.
    """
    try:
        config_content = f'''# --- CONFIGURATION ---
EMAIL_USER = "{credentials.email}"
EMAIL_PASS = "{credentials.password}"
IMAP_SERVER = "imap.gmail.com"
'''
        with open("config.py", "w") as f:
            f.write(config_content)
        return {"status": "success", "message": "Credentials updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
def get_status():
    global ears_process
    if ears_process and ears_process.poll() is None:
        return {"running": True}
    return {"running": False}

@app.get("/logs")
def get_logs():
    return {"logs": list(log_buffer)}

@app.post("/start")
def start_ears():
    global ears_process
    if ears_process and ears_process.poll() is None:
        return {"status": "already_running", "message": "Ears are already listening"}
    
    try:
        # Start ears.py as a subprocess using the current venv python
        # Redirect stdout and stderr to PIPE so we can capture it
        python_executable = sys.executable
        
        # Use unbuffered output (-u) to get logs instantly
        ears_process = subprocess.Popen(
            [python_executable, "-u", "ears.py"], 
            cwd=os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, # Merge stderr into stdout
            text=True,
            bufsize=1, # Line buffered
            encoding='utf-8' # Ensure UTF-8
        )
        
        # Start a thread to read logs
        t = threading.Thread(target=read_process_output, args=(ears_process,))
        t.daemon = True
        t.start()
        
        return {"status": "success", "message": "Ears started listening"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop")
def stop_ears():
    global ears_process
    if ears_process and ears_process.poll() is None:
        ears_process.terminate()
        try:
             ears_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
             ears_process.kill()
        ears_process = None
        return {"status": "success", "message": "Ears stopped listening"}
    return {"status": "not_running", "message": "Ears are not running"}

@app.get("/screenshots")
def get_screenshots():
    # List all png files in current directory
    files = glob.glob("*.png")
    # Sort by modification time, newest first
    files.sort(key=os.path.getmtime, reverse=True)
    return {"screenshots": files}
