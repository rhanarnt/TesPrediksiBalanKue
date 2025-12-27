#!/usr/bin/env python
"""Simple test to verify backend components work"""

import sys
sys.path.insert(0, '.')

print("[1] Importing Flask...")
from flask import Flask, request, jsonify
print("✅ Flask imported")

print("[2] Importing CORS...")
from flask_cors import CORS
print("✅ CORS imported")

print("[3] Importing database components...")
from database import db, init_db, seed_db, User, Bahan, StockRecord
print("✅ Database components imported")

print("[4] Creating Flask app...")
app = Flask(__name__)
print("✅ Flask app created")

print("[5] Configuring database...")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/prediksi_stok_kue'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print("✅ Database configured")

print("[6] Initializing database...")
db.init_app(app)
print("✅ Database init_app done")

print("[7] Setting up CORS...")
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], supports_credentials=True)
print("✅ CORS configured")

print("[8] Adding simple route...")
@app.route('/', methods=['GET'])
def root():
    print("    [ROOT] Request received")
    return jsonify({'status': 'ok', 'message': 'BakeSmart API'}), 200
print("✅ Route added")

print("[9] Initializing DB with app context...")
try:
    with app.app_context():
        print("    [APP_CONTEXT] Entered app context")
        init_db(app)
        print("    [INIT_DB] Database initialized")
        seed_db(app)
        print("    [SEED_DB] Database seeded")
    print("✅ DB initialization complete")
except Exception as e:
    print(f"❌ DB initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("[10] Starting server...")
try:
    from werkzeug.serving import run_simple
    print("✅ About to run_simple on port 5000")
    sys.stdout.flush()
    
    run_simple(
        '127.0.0.1',
        5000,
        app,
        use_debugger=False,
        use_reloader=False,
        threaded=True  # Changed to True for Windows compatibility
    )
except Exception as e:
    print(f"❌ run_simple failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
