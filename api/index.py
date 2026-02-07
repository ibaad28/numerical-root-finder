from flask import Flask, jsonify, request
import numpy as np
import sympy as sp
import json

app = Flask(__name__)

@app.route('/api/root-finder', methods=['POST'])
def root_finder():
    data = request.json
    # Your root finding logic here
    return jsonify({"result": "..."})

# Serverless handler
def handler(event, context):
    return app(event, context)
