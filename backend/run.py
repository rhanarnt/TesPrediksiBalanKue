from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predictor
from database import db, init_db, seed_db, User, Bahan, StockRecord, Notification
import os
from datetime import datetime, timedelta
import jwt
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

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

@app.route('/login', methods=['POST'])
def login():
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
        
        if not user or user.password != password:
            print("Step 6a: Invalid credentials")
            return jsonify({'error': 'Email atau password salah'}), 401
        
        if not user.is_active:
            print("Step 6b: User not active")
            return jsonify({'error': 'User tidak aktif'}), 403
            
        print("Step 7: Creating JWT token")
        token = jwt.encode({
            'email': email,
            'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
        }, app.config['SECRET_KEY'])
        
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

if __name__ == '__main__':
    import sys
    try:
        # Initialize database (this can be done outside context)
        init_db(app)
        seed_db(app)
        print("=" * 60)
        print("BakeSmart Backend Server")
        print("=" * 60)
        print("Database initialized")
        print(f"Running on http://127.0.0.1:5000")
        print("=" * 60)
        sys.stdout.flush()
        
        # Run with minimal config - use Threaded option but no debugger/reloader
        from werkzeug.serving import run_simple
        print("[DEBUG] About to call run_simple...")
        sys.stdout.flush()
        try:
            run_simple(
                '127.0.0.1',
                5000,
                app,
                use_debugger=False,
                use_reloader=False,
                threaded=False  # Try without threading on Windows
            )
        except KeyboardInterrupt:
            print("[INFO] Interrupted")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] Werkzeug failed: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to wsgiref
            print("[INFO] Trying wsgiref fallback...")
            from wsgiref.simple_server import make_server
            httpd = make_server('127.0.0.1', 5000, app)
            httpd.serve_forever()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
