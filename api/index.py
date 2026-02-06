# api/index.py - NO HEAVY IMPORTS
from flask import Flask, request, jsonify
import sympy as sp
import math  # Use built-in math instead of numpy
import json

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html><body>
        <h1>Numerical Root Finder</h1>
        <p>Lightweight API version (no numpy/matplotlib)</p>
        <button onclick="test()">Test Bisection</button>
        <div id="result"></div>
        <script>
        async function test() {
            const res = await fetch('/api/bisection', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    function: "x**2 - 4",
                    a: 0,
                    b: 3,
                    tolerance: 0.0001
                })
            });
            const data = await res.json();
            document.getElementById('result').innerHTML = 
                "Root: " + data.root + " (iterations: " + data.iterations + ")";
        }
        </script>
    </body></html>
    '''

@app.route('/api/bisection', methods=['POST'])
def bisection():
    try:
        data = request.get_json()
        f_str = data.get('function', 'x**2 - 4')
        a = float(data.get('a', 0))
        b = float(data.get('b', 3))
        tol = float(data.get('tolerance', 1e-6))
        max_iter = int(data.get('max_iterations', 100))
        
        # Use sympy for evaluation (no numpy needed)
        x = sp.symbols('x')
        expr = sp.sympify(f_str)
        f = lambda val: float(expr.subs(x, val))
        
        fa, fb = f(a), f(b)
        if fa * fb > 0:
            return jsonify({"error": "f(a) and f(b) must have opposite signs"})
        
        for i in range(max_iter):
            c = (a + b) / 2
            fc = f(c)
            
            if abs(fc) < tol or (b - a) / 2 < tol:
                return jsonify({
                    "root": c,
                    "iterations": i + 1,
                    "error": abs(fc),
                    "function": f_str
                })
            
            if fa * fc < 0:
                b, fb = c, fc
            else:
                a, fa = c, fc
        
        return jsonify({
            "root": (a + b) / 2,
            "iterations": max_iter,
            "error": "Max iterations reached",
            "function": f_str
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def handler(event, context):
    return app(event, context)
