from flask import Flask, request, jsonify
import os
import time

app = Flask(__name__)

@app.route('/')
def hello():
    env = os.getenv('APP_ENV', 'unknown')
    return f"Hello from {env} environment! Version: 1.0.0"

@app.route('/healthz')
def healthz():
    return jsonify({"status": "healthy"}), 200

@app.route('/readyz')
def readyz():
    return jsonify({"status": "ready"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9898)