import subprocess
import time

def run_uvicorn():
    """Runs the Uvicorn server for the FastAPI backend."""
    return subprocess.Popen(
        ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

def run_streamlit():
    """Runs the Streamlit frontend."""
    return subprocess.Popen(
        ["streamlit", "run", "frontend.py", "--server.address=0.0.0.0", "--server.port=8051"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

if __name__ == "__main__":
    backend_process = run_uvicorn()
    time.sleep(5)  # Give backend time to start before frontend
    frontend_process = run_streamlit()

    print("Backend and Frontend started successfully!")

    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
