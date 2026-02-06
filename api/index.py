from flask import Flask, request, jsonify
import sympy as sp
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html><body>
        <h1>Numerical Root Finder API</h1>
        <p>API is working!</p>
        <button onclick="test()">Test API</button>
        <div id="result"></div>
        <script>
        async function test() {
            const res = await fetch('/api/bisection', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({function: "x**2-4", a: 0, b: 3})
            });
            const data = await res.json();
            document.getElementById('result').innerHTML = JSON.stringify(data);
        }
        </script>
    </body></html>
    '''

@app.route('/api/bisection', methods=['POST', 'GET'])
def bisection():
    if request.method == 'GET':
        return jsonify({"message": "Send POST request with JSON data"})
    
    try:
        data = request.get_json() or {}
        f_str = data.get('function', 'x**2 - 4')
        a = float(data.get('a', 0))
        b = float(data.get('b', 3))
        
        # Simple calculation
        x = sp.symbols('x')
        f = sp.lambdify(x, sp.sympify(f_str))
        root = (a + b) / 2  # Simplified for now
        
        return jsonify({
            "function": f_str,
            "root": float(root),
            "message": "Success (simplified calculation)"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "version": "1.0"})

# Vercel requires this
def handler(event, context):
    return app(event, context)

# For local testing
if __name__ == '__main__':
    app.run(port=3000)
