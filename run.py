import subprocess
import sys
import time
import os

# Always use the venv Python so all packages (fastapi, uvicorn, streamlit) are found
VENV_PYTHON = os.path.join(os.path.dirname(__file__), ".venv", "Scripts", "python.exe")
PYTHON = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable

def run():
    print("Starting FastAPI server...")
    server = subprocess.Popen(
        [PYTHON, "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"],
    )
    time.sleep(3)

    print("Starting Streamlit app...")
    streamlit = subprocess.Popen(
        [PYTHON, "-m", "streamlit", "run", "streamlit_app.py", "--server.port", "8501"],
    )

    try:
        streamlit.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.terminate()
        streamlit.terminate()

if __name__ == "__main__":
    if not os.environ.get("GOOGLE_API_KEY"):
        print("WARNING: GOOGLE_API_KEY environment variable not set.")

    run()
