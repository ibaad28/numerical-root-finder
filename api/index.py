# api/index.py - SIMPLE VERSION
from flask import Flask, jsonify
import numpy as np
import sympy as sp
import json

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Numerical Root Finder</h1>
        <p>Streamlit version is not supported on Vercel.</p>
        <p>Use alternative hosting: Render, Railway, or Streamlit Cloud.</p>
        <p>Or use our API endpoints:</p>
        <ul>
            <li><a href="/api/bisection">/api/bisection</a> - POST with JSON</li>
            <li><a href="/api/newton">/api/newton</a> - POST with JSON</li>
        </ul>
    </body>
    </html>
    '''

@app.route('/api/bisection', methods=['POST'])
def bisection():
    # Your root finding code here
    return jsonify({"message": "Bisection method", "status": "working"})

@app.route('/api/newton', methods=['POST'])
def newton():
    # Your root finding code here  
    return jsonify({"message": "Newton's method", "status": "working"})

# Required for Vercel
def handler(event, context):
    return app(event, context)
