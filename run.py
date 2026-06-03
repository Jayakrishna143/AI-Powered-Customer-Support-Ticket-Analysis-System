import subprocess
import sys
import time
import os

def run():
    print("Starting FastAPI server...")
    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    # Give the server a moment to boot
    time.sleep(2)
    print("Server running at http://localhost:8000")

    print("Starting Streamlit app...")
    streamlit = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port", "8501"],
    )

    print("Streamlit running at http://localhost:8501")
    print("\nPress Ctrl+C to stop both.\n")

    try:
        streamlit.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.terminate()
        streamlit.terminate()

if __name__ == "__main__":
    # Check for ANTHROPIC_API_KEY
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        print("Run: export ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)

    run()
