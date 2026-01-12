from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import threading

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Streamlit is running')
        
def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py", "--server.port=8501"])
    
if __name__ == "__main__":
    # Start Streamlit in background
    thread = threading.Thread(target=run_streamlit)
    thread.start()
    
    # Start HTTP server
    server = HTTPServer(('0.0.0.0', 3000), Handler)
    server.serve_forever()