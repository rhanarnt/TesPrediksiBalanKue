#!/usr/bin/env python
"""Minimal Flask backend server without debug mode"""
import sys
import os

# Set production mode FIRST, before any other imports
os.environ['WERKZEUG_RUN_MAIN'] = 'true'
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = '0'

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import jwt
from functools import wraps

# Import database components
from database import db, init_db, seed_db, User, Bahan, StockRecord, Notification
from model import predictor

# Create Flask app
app = Flask(__name__)
app.debug = False

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/prediksi_stok_kue'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
app.config['SECRET_KEY'] = 'rahasia-sangat-rahasia'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize database
db.init_app(app)

# Configure CORS
CORS(app, 
     origins="*",
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True)

# JWT decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
            
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(email=data['email']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# ROOT route
@app.route('/', methods=['GET'])
def root():
    return jsonify({'status': 'ok', 'message': 'BakeSmart API'}), 200

# LOGIN route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email dan password diperlukan'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user or user.password != password:
        return jsonify({'error': 'Email atau password salah'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'User tidak aktif'}), 403
    
    token = jwt.encode({
        'email': user.email,
        'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({
        'message': 'Login berhasil',
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name
        }
    }), 200

# STOCK RECORDS route
@app.route('/stock-records', methods=['GET'])
@token_required
def get_stock_records(current_user):
    try:
        # Get all stock records with bahan nama from JOIN
        records = db.session.query(
            StockRecord.id,
            StockRecord.bahan_id,
            Bahan.nama.label('nama_bahan'),
            StockRecord.jumlah,
            Bahan.unit,
            StockRecord.tipe,
            StockRecord.tanggal,
            StockRecord.catatan
        ).join(Bahan, StockRecord.bahan_id == Bahan.id).all()
        
        data = []
        for record in records:
            data.append({
                'id': record.id,
                'bahan_id': record.bahan_id,
                'nama_bahan': record.nama_bahan,
                'jumlah': record.jumlah,
                'unit': record.unit,
                'tipe': record.tipe,
                'tanggal': record.tanggal.isoformat() if record.tanggal else None,
                'catatan': record.catatan
            })
        
        return jsonify({'data': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CREATE STOCK RECORD route
@app.route('/stock-record', methods=['POST'])
@token_required
def create_stock_record(current_user):
    try:
        data = request.get_json()
        
        # Support both bahan_id and bahan_nama
        bahan_id = data.get('bahan_id')
        bahan_nama = data.get('bahan_nama')
        
        # If bahan_nama is provided, find or create bahan
        if bahan_nama and not bahan_id:
            bahan = Bahan.query.filter_by(nama=bahan_nama).first()
            if not bahan:
                # Create new bahan if it doesn't exist
                bahan = Bahan(
                    nama=bahan_nama,
                    unit=data.get('unit', 'Kilogram (kg)'),
                    stok_minimum=0,
                    stok_optimal=100,
                    harga_per_unit=0
                )
                db.session.add(bahan)
                db.session.flush()  # Get ID before commit
            bahan_id = bahan.id
        
        # Create stock record
        record = StockRecord(
            bahan_id=bahan_id,
            jumlah=data.get('jumlah'),
            unit=data.get('unit', 'Kilogram (kg)'),
            tipe=data.get('tipe'),
            catatan=data.get('catatan', ''),
            tanggal=datetime.utcnow()
        )
        
        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            'message': 'Stock record berhasil dibuat',
            'data': {
                'id': record.id,
                'bahan_id': record.bahan_id,
                'jumlah': record.jumlah,
                'unit': record.unit,
                'tipe': record.tipe,
                'tanggal': record.tanggal.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# STOK (ingredients list) route
@app.route('/stok', methods=['GET'])
@token_required
def get_stok(current_user):
    try:
        bahans = Bahan.query.all()
        data = []
        for bahan in bahans:
            data.append({
                'id': bahan.id,
                'nama': bahan.nama,
                'unit': bahan.unit,
                'stok_minimum': bahan.stok_minimum,
                'stok_optimal': bahan.stok_optimal,
                'harga_per_unit': bahan.harga_per_unit
            })
        return jsonify({'data': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        # Initialize database
        init_db(app)
        seed_db(app)
        
        print("=" * 60)
        print("BakeSmart Backend Server")
        print("=" * 60)
        print("Database initialized")
        print(f"Running on http://127.0.0.1:5000")
        print("=" * 60)
        sys.stdout.flush()
        
        # Try to use waitress first (best choice)
        try:
            from waitress import serve
            print("[INFO] Starting with waitress server")
            sys.stdout.flush()
            serve(app, host='127.0.0.1', port=5000, threads=4, _quiet=False)
        except Exception as e:
            print(f"[ERROR] Waitress failed: {e}")
            print("[INFO] Trying wsgiref fallback...")
            from wsgiref.simple_server import make_server
            httpd = make_server('127.0.0.1', 5000, app)
            print("[INFO] WSGIRef server started")
            sys.stdout.flush()
            httpd.serve_forever()
    except Exception as e:
        print(f"[FATAL] Server failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
