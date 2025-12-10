#!/usr/bin/env python
"""
Minimal test server - absolute bare minimum untuk debug
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

try:
    from flask import Flask, jsonify
    print("[1] Flask imported")
    
    app = Flask(__name__)
    print("[2] Flask app created")
    
    @app.route('/test', methods=['GET'])
    def test():
        return jsonify({'status': 'ok'})
    
    @app.route('/login', methods=['POST'])
    def login():
        return jsonify({'status': 'ok'})
    
    print("[3] Routes registered")
    
    if __name__ == '__main__':
        print("[4] Starting server...")
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False, threaded=False)
        
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
