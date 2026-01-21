"""
Authentication module for BakeSmart API
Handles JWT token generation and user authentication
"""
import os
import jwt
import hashlib
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

# Secret key untuk JWT (gunakan env var di production)
SECRET_KEY = os.getenv("JWT_SECRET", "bakesmart-secret-key-2026")
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", "24"))


def hash_password(password: str) -> str:
    """Hash password dengan SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verifikasi password"""
    return hash_password(password) == hashed


def generate_jwt_token(user_id: int, email: str) -> str:
    """Generate JWT token"""
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_jwt_token(token: str) -> dict | None:
    """Decode dan validate JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


def get_token_from_header() -> str | None:
    """Extract JWT token dari Authorization header"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header[7:]  # Remove "Bearer " prefix


def require_auth(f):
    """Decorator untuk melindungi endpoint dengan JWT"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        if not token:
            return {"error": "Token tidak ditemukan di header Authorization"}, 401

        payload = decode_jwt_token(token)
        if not payload:
            return {"error": "Token invalid atau expired"}, 401

        # Pass user info ke function
        request.user_id = payload.get("user_id")
        request.user_email = payload.get("email")
        return f(*args, **kwargs)

    return decorated_function


# ============================
#  Database functions
# ============================

def get_db_config():
    """Get database config dari env vars"""
    return {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "prediksi_kue"),
    }


def get_db_connection():
    """Get MySQL connection"""
    cfg = get_db_config()
    try:
        conn = mysql.connector.connect(
            host=cfg["host"],
            port=cfg["port"],
            user=cfg["user"],
            password=cfg["password"],
            database=cfg["database"],
            autocommit=True,
        )
        return conn
    except Error as e:
        print(f"[auth] MySQL Connection Error: {e}")
        return None


def ensure_users_table():
    """Pastikan tabel users ada di database"""
    cfg = get_db_config()
    try:
        # Connect without database first
        conn = mysql.connector.connect(
            host=cfg["host"],
            port=cfg["port"],
            user=cfg["user"],
            password=cfg["password"],
            autocommit=True,
        )
    except Error as e:
        print(f"[auth] Failed to connect to MySQL: {e}")
        return False

    try:
        cur = conn.cursor()
        # Create database if not exists
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{cfg['database']}` CHARACTER SET utf8mb4;"
        )
        cur.close()
        conn.close()
    except Error as e:
        print(f"[auth] Failed to create database: {e}")
        try:
            conn.close()
        except:
            pass
        return False

    # Connect to database and create users table
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(128),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        )

        # Insert default admin user jika belum ada
        try:
            admin_pass_hash = hash_password("admin123")
            cur.execute(
                """
                INSERT INTO users (email, password, name)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE name=VALUES(name)
                """,
                ("admin@bakesmart.com", admin_pass_hash, "Admin BakeSmart"),
            )
            print("[auth] Default admin user ensured: admin@bakesmart.com / admin123")
        except Error as e:
            # User might already exist
            pass

        cur.close()
        conn.close()
        print("[auth] Users table ensured.")
        return True
    except Error as e:
        print(f"[auth] Failed to create users table: {e}")
        return False


def find_user_by_email(email: str) -> dict | None:
    """Cari user berdasarkan email"""
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT id, email, password, name FROM users WHERE email = %s",
            (email,),
        )
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    except Error as e:
        print(f"[auth] find_user_by_email error: {e}")
        return None


def authenticate_user(email: str, password: str) -> dict | None:
    """Autentikasi user, return user info jika berhasil"""
    user = find_user_by_email(email)
    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
    }
