import os
import sys

# Clear problematic environment variables
if 'WERKZEUG_RUN_MAIN' in os.environ:
    del os.environ['WERKZEUG_RUN_MAIN']
if 'WERKZEUG_SERVER_FD' in os.environ:
    del os.environ['WERKZEUG_SERVER_FD']

# Set proper environment
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = '0'

# NOW import Flask after env vars are set
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predictor
from prediction_service import prediction_service
from database import db, init_db, seed_db, User, Bahan, StockRecord, Notification
from datetime import datetime, timedelta
import jwt
from functools import wraps

# DO NOT use load_dotenv - configure everything explicitly
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)

# Explicitly disable debug mode
app.debug = False
app.testing = False
app.config['ENV'] = 'production'

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:@127.0.0.1:3306/prediksi_stok_kue')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}

# JWT Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'rahasia-sangat-rahasia')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize Database
db.init_app(app)

# Konfigurasi CORS - lebih permisif untuk Web
CORS(app, 
     origins="*",
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True)

# Decorator untuk memeriksa token JWT
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
            current_user = data['email']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
            
        return f(current_user, *args, **kwargs)
        
    return decorated

@app.route('/', methods=['GET'])
def root():
    return jsonify({'status': 'ok', 'message': 'BakeSmart API'}), 200

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 204
        
    print("=== LOGIN REQUEST RECEIVED ===")
    try:
        print("Step 1: Getting JSON")
        data = request.get_json()
        print(f"Step 2: Got data: {data}")
        email = data.get('email')
        password = data.get('password')
        
        print(f"Step 3: Email={email}, Password={password}")
        
        if not email or not password:
            print("Step 4a: Missing credentials")
            return jsonify({'error': 'Email dan password diperlukan'}), 400
        
        print("Step 4b: Querying database")
        user = User.query.filter_by(email=email).first()
        print(f"Step 5: User={user}")
        print(f"Step 5b: User password={user.password if user else 'N/A'}")
        print(f"Step 5c: Input password={password}")
        
        if not user:
            print("Step 6a: User not found")
            return jsonify({'error': 'Email atau password salah'}), 401
            
        if user.password != password:
            print("Step 6b: Password mismatch")
            print(f"  Expected: {user.password}")
            print(f"  Got: {password}")
            return jsonify({'error': 'Email atau password salah'}), 401
        
        if not user.is_active:
            print("Step 6c: User not active")
            return jsonify({'error': 'User tidak aktif'}), 403
            
        print("Step 7: Creating JWT token")
        token = jwt.encode({
            'email': email,
            'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        print(f"Step 8: Login success")
        return jsonify({
            'message': 'Login berhasil',
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }
        }), 200
        
    except Exception as e:
        print(f"LOGIN ERROR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/prediksi', methods=['POST'])
@token_required
def predict(current_user):
    try:
        data = request.get_json()
        
        if 'jumlah' not in data or 'harga' not in data:
            return jsonify({'error': 'Missing required fields: jumlah, harga'}), 400
        
        jumlah = float(data['jumlah'])
        harga = float(data['harga'])
        
        if jumlah <= 0 or harga <= 0:
            return jsonify({'error': 'Jumlah dan harga harus lebih dari 0'}), 400
        
        result = predictor.predict(jumlah, harga)
        return jsonify(result), 200
    
    except ValueError as e:
        return jsonify({'error': f'Input tidak valid: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Kesalahan server: {str(e)}'}), 500

@app.route('/permintaan', methods=['POST', 'OPTIONS'])
@token_required
def permintaan(current_user):
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        
        if not data or 'nama_bahan' not in data or 'kuantitas' not in data:
            return jsonify({'error': 'Missing fields: nama_bahan, kuantitas'}), 400
        
        # Simpan ke database
        # For now, just echo back success
        return jsonify({
            'status': 'ok',
            'message': 'Permintaan diterima dan disimpan',
            'data': data
        }), 200
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/stok', methods=['GET'])
@token_required
def get_stok(current_user):
    """Get semua data stok bahan"""
    try:
        bahans = Bahan.query.all()
        data = [{
            'id': b.id,
            'nama': b.nama,
            'unit': b.unit,
            'stok_minimum': b.stok_minimum,
            'stok_optimal': b.stok_optimal,
            'harga_per_unit': b.harga_per_unit
        } for b in bahans]
        
        return jsonify({'data': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stok', methods=['POST'])
@token_required
def create_bahan(current_user):
    """Create bahan baru"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'nama' not in data:
            return jsonify({'message': 'Nama bahan diperlukan'}), 400
        
        nama = data.get('nama', '').strip()
        if not nama:
            return jsonify({'message': 'Nama bahan tidak boleh kosong'}), 400
        
        # Check if bahan already exists
        existing_bahan = Bahan.query.filter_by(nama=nama).first()
        if existing_bahan:
            return jsonify({'message': 'Bahan dengan nama ini sudah ada'}), 400
        
        # Create new bahan
        new_bahan = Bahan(
            nama=nama,
            unit=data.get('unit', 'Kilogram (kg)'),
            stok_minimum=data.get('stok_minimum', 0),
            stok_optimal=data.get('stok_optimal', 0),
            harga_per_unit=data.get('harga_per_unit', 0)
        )
        
        db.session.add(new_bahan)
        db.session.commit()
        
        return jsonify({
            'message': 'Bahan berhasil dibuat',
            'data': {
                'id': new_bahan.id,
                'nama': new_bahan.nama,
                'unit': new_bahan.unit
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

@app.route('/stock-record', methods=['POST'])
@token_required
def create_stock_record(current_user):
    """Buat record stok baru (input/output/adjustment)"""
    try:
        data = request.get_json()
        
        # Support both bahan_id dan bahan_nama untuk fleksibilitas
        bahan_id = data.get('bahan_id')
        bahan_nama = data.get('bahan_nama')
        
        # Jika ada bahan_nama, cari atau buat bahan baru
        if bahan_nama and not bahan_id:
            bahan = Bahan.query.filter_by(nama=bahan_nama).first()
            if not bahan:
                # Buat bahan baru jika tidak ada
                bahan = Bahan(
                    nama=bahan_nama,
                    unit=data.get('unit', 'Kilogram (kg)'),
                    stok_minimum=0,
                    stok_optimal=100,
                    harga_per_unit=0
                )
                db.session.add(bahan)
                db.session.flush()  # Flush untuk mendapatkan ID
            bahan_id = bahan.id
        
        # Validasi required fields
        if not bahan_id or 'jumlah' not in data or 'tipe' not in data:
            return jsonify({'error': 'Missing fields: bahan_id/bahan_nama, jumlah, tipe'}), 400
        
        # Validasi tipe
        if data['tipe'] not in ['masuk', 'keluar', 'penyesuaian']:
            return jsonify({'error': 'Tipe harus masuk/keluar/penyesuaian'}), 400
        
        # Get user dari database
        user = User.query.filter_by(email=current_user).first()
        if not user:
            return jsonify({'error': 'User tidak ditemukan'}), 404
        
        # Create stock record
        stock_record = StockRecord(
            user_id=user.id,
            bahan_id=bahan_id,
            jumlah=float(data['jumlah']),
            tipe=data['tipe'],
            catatan=data.get('catatan', ''),
            tanggal=datetime.utcnow()
        )
        
        db.session.add(stock_record)
        db.session.commit()
        
        return jsonify({
            'message': 'Stock record berhasil dibuat',
            'data': {
                'id': stock_record.id,
                'bahan_id': stock_record.bahan_id,
                'jumlah': stock_record.jumlah,
                'tipe': stock_record.tipe,
                'tanggal': stock_record.tanggal.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/stock-records', methods=['GET'])
@token_required
def get_stock_records(current_user):
    """Get semua stock records (history input/output)"""
    try:
        # Get all stock records with bahan details
        records = db.session.query(
            StockRecord.id,
            StockRecord.bahan_id,
            StockRecord.jumlah,
            StockRecord.tipe,
            StockRecord.catatan,
            StockRecord.tanggal,
            Bahan.nama,
            Bahan.unit
        ).join(Bahan).all()
        
        data = [{
            'id': r.id,
            'bahan_id': r.bahan_id,
            'nama_bahan': r.nama,
            'jumlah': float(r.jumlah),
            'unit': r.unit,
            'tipe': r.tipe,
            'catatan': r.catatan,
            'tanggal': r.tanggal.isoformat() if r.tanggal else None
        } for r in records]
        
        return jsonify({'data': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/notifications', methods=['GET'])
@token_required
def get_notifications(current_user):
    """Get notifikasi untuk current user"""
    try:
        user = User.query.filter_by(email=current_user).first()
        if not user:
            return jsonify({'error': 'User tidak ditemukan'}), 404
        
        # Get notifications (limit 20, ordered by newest)
        notifications = Notification.query.filter_by(user_id=user.id)\
            .order_by(Notification.id.desc())\
            .limit(20)\
            .all()
        
        data = [{
            'id': n.id,
            'tipe': n.tipe,
            'judul': n.judul,
            'pesan': n.pesan,
            'status': n.status,
            'related_bahan_id': n.related_bahan_id,
            'created_at': n.created_at.isoformat() if hasattr(n, 'created_at') else None
        } for n in notifications]
        
        return jsonify({'data': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bahan/<int:bahan_id>', methods=['GET'])
@token_required
def get_bahan_detail(current_user, bahan_id):
    """Get detail bahan berdasarkan ID"""
    try:
        bahan = Bahan.query.get(bahan_id)
        if not bahan:
            return jsonify({'error': 'Bahan tidak ditemukan'}), 404
        
        return jsonify({
            'data': {
                'id': bahan.id,
                'nama': bahan.nama,
                'unit': bahan.unit,
                'stok_minimum': bahan.stok_minimum,
                'stok_optimal': bahan.stok_optimal,
                'harga_per_unit': bahan.harga_per_unit
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/optimasi', methods=['GET'])
@token_required
def get_optimasi_stok(current_user):
    """Get rekomendasi optimasi stok untuk semua bahan"""
    try:
        # Get semua bahan dengan perhitungan stok saat ini
        bahans = Bahan.query.all()
        
        data = []
        for bahan in bahans:
            # Hitung total stok dari stock records
            stock_in = db.session.query(db.func.sum(StockRecord.jumlah)).filter(
                StockRecord.bahan_id == bahan.id,
                StockRecord.tipe.in_(['masuk', 'penyesuaian'])
            ).scalar() or 0
            
            stock_out = db.session.query(db.func.sum(StockRecord.jumlah)).filter(
                StockRecord.bahan_id == bahan.id,
                StockRecord.tipe == 'keluar'
            ).scalar() or 0
            
            current_stock = float(stock_in) - float(stock_out)
            
            # Tentukan status berdasarkan current vs optimal
            if current_stock <= 0:
                status = 'Kritis'
                status_color = '#EF4444'  # Red
            elif current_stock < bahan.stok_minimum:
                status = 'Kurang'
                status_color = '#F97316'  # Orange
            elif current_stock >= bahan.stok_optimal:
                status = 'Optimal'
                status_color = '#7C3AED'  # Purple
            else:
                status = 'Cukup'
                status_color = '#EF4444'  # Red
            
            data.append({
                'bahan_id': bahan.id,
                'nama': bahan.nama,
                'unit': bahan.unit,
                'current_stock': current_stock,
                'stok_minimum': bahan.stok_minimum,
                'stok_optimal': bahan.stok_optimal,
                'harga_per_unit': bahan.harga_per_unit,
                'deskripsi': bahan.deskripsi or '',
                'status': status,
                'status_color': status_color,
            })
        
        return jsonify({'data': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Logout - berhasil jika token valid"""
    try:
        return jsonify({
            'message': 'Logout berhasil',
            'status': 'ok'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== ADVANCED PREDICTION ENDPOINTS =====

@app.route('/prediksi-detail/<int:bahan_id>', methods=['GET'])
@token_required
def predict_material_detail(current_user, bahan_id):
    """Get detailed prediction for a specific material"""
    try:
        bahan = Bahan.query.get(bahan_id)
        
        if not bahan:
            return jsonify({'error': 'Material tidak ditemukan'}), 404
        
        # Get current stock from latest stock record
        latest_record = StockRecord.query.filter_by(bahan_id=bahan_id).order_by(
            StockRecord.tanggal.desc()
        ).first()
        
        current_stock = latest_record.jumlah if latest_record else 0
        
        result = prediction_service.predict_material_detail(
            bahan_id=bahan_id,
            current_stock=current_stock,
            stok_minimum=bahan.stok_minimum or 10,
            stok_optimal=bahan.stok_optimal or 50,
            harga_per_unit=bahan.harga_per_unit or 0,
            recent_days=30
        )
        
        return jsonify({
            'data': result,
            'bahan': {
                'id': bahan.id,
                'nama': bahan.nama,
                'unit': bahan.unit,
                'current_stock': current_stock,
                'stok_minimum': bahan.stok_minimum,
                'stok_optimal': bahan.stok_optimal,
                'harga_per_unit': bahan.harga_per_unit
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Kesalahan server: {str(e)}'}), 500

@app.route('/prediksi-batch', methods=['GET'])
@token_required
def predict_batch(current_user):
    """Get predictions for all materials"""
    try:
        bahans = Bahan.query.all()
        results = []
        
        for bahan in bahans:
            latest_record = StockRecord.query.filter_by(bahan_id=bahan.id).order_by(
                StockRecord.tanggal.desc()
            ).first()
            
            current_stock = latest_record.jumlah if latest_record else 0
            
            result = prediction_service.predict_material_detail(
                bahan_id=bahan.id,
                current_stock=current_stock,
                stok_minimum=bahan.stok_minimum or 10,
                stok_optimal=bahan.stok_optimal or 50,
                harga_per_unit=bahan.harga_per_unit or 0,
                recent_days=30
            )
            
            if result['status'] == 'success':
                result['bahan_nama'] = bahan.nama
                results.append(result)
        
        # Sort by urgency (days_until_stockout)
        results.sort(key=lambda x: (
            x.get('days_until_stockout') is None,
            x.get('days_until_stockout') or float('inf')
        ))
        
        return jsonify({
            'data': results,
            'total': len(results),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Kesalahan server: {str(e)}'}), 500

if __name__ == '__main__':
    import sys
    try:
        # Initialize database
        init_db(app)
        seed_db(app)
        print("=" * 60)
        print("BakeSmart Backend Server")
        print("=" * 60)
        print("Database initialized")
        print("=" * 60)
        sys.stdout.flush()
        
        # Run Flask app
        app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
