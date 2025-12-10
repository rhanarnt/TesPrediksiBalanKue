"""
Database configuration dan models menggunakan SQLAlchemy
Support untuk PostgreSQL dan SQLite
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

# ============================================================================
# MODELS
# ============================================================================

class User(db.Model):
    """Model untuk User/Pengguna"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stock_records = db.relationship('StockRecord', backref='user', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'


class Bahan(db.Model):
    """Model untuk Bahan Baku"""
    __tablename__ = 'bahans'
    
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(120), nullable=False, unique=True, index=True)
    unit = db.Column(db.String(20), nullable=False)  # kg, liter, butir, etc
    stok_minimum = db.Column(db.Float, default=0)
    stok_optimal = db.Column(db.Float, default=0)
    harga_per_unit = db.Column(db.Float, default=0)
    deskripsi = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stock_records = db.relationship('StockRecord', backref='bahan', lazy=True, cascade='all, delete-orphan')
    predictions = db.relationship('Prediction', backref='bahan', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Bahan {self.nama}>'


class StockRecord(db.Model):
    """Model untuk Catatan Stok"""
    __tablename__ = 'stock_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bahan_id = db.Column(db.Integer, db.ForeignKey('bahans.id'), nullable=False)
    jumlah = db.Column(db.Float, nullable=False)
    tipe = db.Column(db.String(20), nullable=False)  # 'masuk', 'keluar', 'penyesuaian'
    catatan = db.Column(db.Text)
    tanggal = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<StockRecord {self.bahan.nama} {self.jumlah}>'


class Prediction(db.Model):
    """Model untuk Prediksi Permintaan"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    bahan_id = db.Column(db.Integer, db.ForeignKey('bahans.id'), nullable=False)
    prediksi_jumlah = db.Column(db.Float, nullable=False)
    akurasi = db.Column(db.Float)  # 0-100
    periode_mulai = db.Column(db.DateTime, nullable=False)
    periode_akhir = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, used
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Prediction {self.bahan.nama}>'


class Order(db.Model):
    """Model untuk Pesanan Bahan"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    bahan_id = db.Column(db.Integer, db.ForeignKey('bahans.id'), nullable=False)
    jumlah = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, received, cancelled
    tanggal_pesan = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    tanggal_kirim_estimasi = db.Column(db.DateTime)
    tanggal_terima = db.Column(db.DateTime)
    supplier = db.Column(db.String(120))
    harga_total = db.Column(db.Float)
    catatan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Order {self.bahan.nama} - {self.status}>'


class Notification(db.Model):
    """Model untuk Notifikasi"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tipe = db.Column(db.String(50), nullable=False)  # stok_rendah, pesanan_ulang, prediksi_tinggi, dll
    judul = db.Column(db.String(255), nullable=False)
    pesan = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='unread')  # unread, read
    related_bahan_id = db.Column(db.Integer, db.ForeignKey('bahans.id'))
    data_json = db.Column(db.JSON)  # Menyimpan data tambahan sebagai JSON
    dibuat_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    dibaca_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Notification {self.tipe}>'


class AuditLog(db.Model):
    """Model untuk Audit Log (tracking perubahan)"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(50), nullable=False)  # CREATE, UPDATE, DELETE
    table_name = db.Column(db.String(50), nullable=False)
    record_id = db.Column(db.Integer)
    old_values = db.Column(db.JSON)
    new_values = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<AuditLog {self.action} on {self.table_name}>'


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_db(app):
    """Inisialisasi database"""
    with app.app_context():
        db.create_all()
        print("[OK] Database initialized successfully")


def seed_db(app):
    """Seed initial data"""
    with app.app_context():
        # Check if data already exists
        if Bahan.query.first() is not None:
            print("[INFO] Database already seeded")
            return
        
        # Add default bahans
        bahans_data = [
            {
                'nama': 'Tepung Terigu Serbaguna',
                'unit': 'kg',
                'stok_minimum': 50,
                'stok_optimal': 200,
                'harga_per_unit': 5000,
                'deskripsi': 'Tepung terigu berkualitas tinggi untuk semua jenis kue'
            },
            {
                'nama': 'Gula Halus',
                'unit': 'kg',
                'stok_minimum': 20,
                'stok_optimal': 80,
                'harga_per_unit': 8000,
                'deskripsi': 'Gula halus premium'
            },
            {
                'nama': 'Telur Ayam',
                'unit': 'butir',
                'stok_minimum': 50,
                'stok_optimal': 120,
                'harga_per_unit': 1500,
                'deskripsi': 'Telur ayam segar'
            },
            {
                'nama': 'Susu Cair',
                'unit': 'liter',
                'stok_minimum': 10,
                'stok_optimal': 60,
                'harga_per_unit': 12000,
                'deskripsi': 'Susu cair murni'
            },
            {
                'nama': 'Mentega',
                'unit': 'kg',
                'stok_minimum': 5,
                'stok_optimal': 50,
                'harga_per_unit': 35000,
                'deskripsi': 'Mentega berkualitas'
            },
        ]
        
        for data in bahans_data:
            bahan = Bahan(**data)
            db.session.add(bahan)
        
        # Add default user
        user = User(
            email='admin@bakesmart.com',
            password='admin123',  # In production, use hashing!
            name='Admin BakeSmart',
            phone='081234567890'
        )
        db.session.add(user)
        
        db.session.commit()
        print("[OK] Database seeded with initial data")
