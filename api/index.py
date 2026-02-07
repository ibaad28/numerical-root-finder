from flask import Flask, request, jsonify
import numpy as np
import sympy as sp
import json

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Numerical Root Finder API</title>
    </head>
    <body>
        <h1>Numerical Root Finder API</h1>
        <p>Use POST requests to <code>/api/root-finder</code></p>
        <button onclick="test()">Test API</button>
        <div id="result"></div>
        <script>
        async function test() {
            const response = await fetch('/api/root-finder', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    function: "x**2 - 4",
                    method: "bisection",
                    a: 0,
                    b: 3,
                    tolerance: 0.0001
                })
            });
            const data = await response.json();
            document.getElementById('result').innerHTML = 
                'Result: ' + JSON.stringify(data);
        }
        </script>
    </body>
    </html>
    '''

@app.route('/api/root-finder', methods=['POST'])
def root_finder():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Simple test calculation
        func_str = data.get('function', 'x**2 - 4')
        
        # Use sympy to evaluate
        x = sp.symbols('x')
        expr = sp.sympify(func_str)
        
        # Test at midpoint
        a = float(data.get('a', 0))
        b = float(data.get('b', 3))
        midpoint = (a + b) / 2
        value = float(expr.subs(x, midpoint))
        
        return jsonify({
            "success": True,
            "function": func_str,
            "midpoint": midpoint,
            "value_at_midpoint": value,
            "message": "Test calculation successful"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Calculation failed"
        }), 400

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "Numerical Root Finder API",
        "version": "1.0"
    })

# Vercel serverless function handler
def handler(event, context):
    from flask import Response
    
    # Convert Vercel event to Flask request
    with app.request_context({
        'path': event['path'],
        'method': event['httpMethod'],
        'headers': event.get('headers', {}),
        'query_string': event.get('queryStringParameters', {}),
        'body': event.get('body', '')
    }):
        # Process the request
        response = app.full_dispatch_request()
        
        # Convert Flask response to Vercel format
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }

# For local testing only
if __name__ == '__main__':
    app.run(debug=True, port=3000)
