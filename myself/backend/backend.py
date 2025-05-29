from flask import Flask, jsonify, request
import socket
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
    hostname = socket.gethostname()
    return jsonify({
        'message': 'Hello from K8s Ingress test backend - Root Path',
        'hostname': hostname,
        'pod_ip': os.environ.get('POD_IP', 'unknown'),
        'path': '/'
    })

@app.route('/api')
def api():
    hostname = socket.gethostname()
    return jsonify({
        'message': 'Hello from K8s Ingress API endpoint',
        'hostname': hostname,
        'pod_ip': os.environ.get('POD_IP', 'unknown'),
        'path': '/api'
    })

@app.route('/api/v1/users')
def users():
    hostname = socket.gethostname()
    return jsonify({
        'message': 'User API - Version 1',
        'hostname': hostname,
        'pod_ip': os.environ.get('POD_IP', 'unknown'),
        'path': '/api/v1/users',
        'data': [
            {'id': 1, 'name': 'User 1'},
            {'id': 2, 'name': 'User 2'}
        ]
    })

@app.route('/api/v1/products')
def products():
    hostname = socket.gethostname()
    return jsonify({
        'message': 'Products API - Version 1',
        'hostname': hostname,
        'pod_ip': os.environ.get('POD_IP', 'unknown'),
        'path': '/api/v1/products',
        'data': [
            {'id': 1, 'name': 'Product 1'},
            {'id': 2, 'name': 'Product 2'}
        ]
    })

@app.route('/api/v2/status')
def status():
    hostname = socket.gethostname()
    return jsonify({
        'message': 'Status API - Version 2',
        'hostname': hostname,
        'pod_ip': os.environ.get('POD_IP', 'unknown'),
        'path': '/api/v2/status',
        'status': 'running',
        'timestamp': time.time()
    })

@app.route('/app/dashboard')
def dashboard():
    hostname = socket.gethostname()
    return jsonify({
        'message': 'Dashboard Application',
        'hostname': hostname,
        'pod_ip': os.environ.get('POD_IP', 'unknown'),
        'path': '/app/dashboard'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok'
    })

# 通配符路径，用于测试路径匹配
@app.route('/<path:subpath>')
def catch_all(subpath):
    hostname = socket.gethostname()
    return jsonify({
        'message': 'Catch-all handler',
        'hostname': hostname,
        'pod_ip': os.environ.get('POD_IP', 'unknown'),
        'requested_path': subpath,
        'request_headers': dict(request.headers)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
