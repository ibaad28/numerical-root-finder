from http.server import BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "healthy",
            "service": "Numerical Root Finder API",
            "version": "1.0"
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            # Simple test response
            response = {
                "success": True,
                "message": "API is working!",
                "received_data": data,
                "test_calculation": "x^2 - 4 evaluated at x=2 gives 0"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {
                "success": False,
                "error": str(e),
                "message": "Invalid JSON or processing error"
            }
            self.wfile.write(json.dumps(error_response).encode())

# Vercel requires this exact structure
def handler(request, context):
    """
    Vercel serverless function handler
    request: Vercel request object
    context: Vercel context object
    """
    from io import BytesIO
    
    # Create a mock HTTP request handler
    class VercelHTTPRequest(BaseHTTPRequestHandler):
        def __init__(self, request):
            self.request = request
            self.headers = self.parse_headers()
            self.rfile = BytesIO(request.get('body', '').encode() if request.get('body') else b'')
            self.wfile = BytesIO()
            self.path = request.get('path', '/')
            self.command = request.get('httpMethod', 'GET')
            
        def parse_headers(self):
            headers = self.request.get('headers', {})
            # Convert to lowercase keys for HTTP protocol
            return {k.lower(): v for k, v in headers.items()}
        
        def send_response(self, code):
            self.status_code = code
            
        def send_header(self, key, value):
            if not hasattr(self, 'response_headers'):
                self.response_headers = {}
            self.response_headers[key] = value
            
        def end_headers(self):
            pass
        
        def log_message(self, format, *args):
            pass  # Silence logging
    
    # Process the request
    vercel_request = VercelHTTPRequest(request)
    
    if request.get('httpMethod') == 'GET':
        vercel_request.do_GET()
    elif request.get('httpMethod') == 'POST':
        vercel_request.do_POST()
    else:
        vercel_request.send_response(405)
        vercel_request.send_header('Content-type', 'application/json')
        vercel_request.end_headers()
        vercel_request.wfile.write(json.dumps({
            "error": "Method not allowed",
            "allowed_methods": ["GET", "POST"]
        }).encode())
    
    # Return Vercel response
    return {
        'statusCode': getattr(vercel_request, 'status_code', 200),
        'headers': getattr(vercel_request, 'response_headers', {'Content-Type': 'application/json'}),
        'body': vercel_request.wfile.getvalue().decode('utf-8')
    }
