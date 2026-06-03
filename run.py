import subprocess
import sys
import time

def run():
    print("Starting FastAPI server...")
    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
    )
    time.sleep(2)

    print("Starting Streamlit app...")
    streamlit = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port", "8501"]
    )
    streamlit.wait()

if __name__ == "__main__":
    run()
