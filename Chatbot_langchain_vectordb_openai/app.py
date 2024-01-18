from flask import Flask, render_template
import subprocess
from threading import Thread

app = Flask(__name__)

def run_streamlit_app():
    subprocess.run(["streamlit", "run", "chatbot_strmlt.py", "--server.port", "8500"])
if __name__ == '__main__':
    # Start Streamlit app in a separate thread
    streamlit_thread = Thread(target=run_streamlit_app)
    streamlit_thread.start()
    
    # Run Flask app on a specific port (e.g., 5000)
    app.run(debug=True, port=5000)

    # Wait for the Streamlit thread to finish
    streamlit_thread.join()