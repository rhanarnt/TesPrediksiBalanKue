import os
import mysql.connector
from mysql.connector import Error

# Env vars: DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def get_config():
    return {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "prediksi_kue"),
    }


def get_connection():
    cfg = get_config()
    try:
        conn = mysql.connector.connect(
            host=cfg["host"], port=cfg["port"], user=cfg["user"],
            password=cfg["password"], database=cfg["database"], autocommit=True
        )
        return conn
    except Error as e:
        print(f"[db] Koneksi MySQL gagal: {e}")
        return None


def ensure_database():
    """Pastikan database ada. Jika tidak, buat otomatis."""
    cfg = get_config()
    try:
        # coba konek tanpa database terlebih dahulu
        conn = mysql.connector.connect(
            host=cfg["host"], port=cfg["port"], user=cfg["user"], password=cfg["password"], autocommit=True
        )
    except Error as e:
        print(f"[db] Gagal konek ke MySQL (tanpa DB): {e}")
        return False
    try:
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{cfg['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cur.close()
        conn.close()
        return True
    except Error as e:
        print(f"[db] Gagal membuat database: {e}")
        try:
            conn.close()
        except Exception:
            pass
        return False


def init_db():
    # pastikan DB ada
    if not ensure_database():
        return False
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                jumlah DOUBLE NOT NULL,
                harga DOUBLE NOT NULL,
                prediksi_permintaan DOUBLE NOT NULL,
                status_stok VARCHAR(64) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        )
        # Tabel stok untuk integrasi Flutter (CRUD stok)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS stocks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(128) NOT NULL UNIQUE,
                qty DOUBLE NOT NULL DEFAULT 0,
                unit VARCHAR(16) NOT NULL DEFAULT 'kg',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        )
        cur.close()
        conn.close()
        print("[db] Tabel predictions siap.")
        return True
    except Error as e:
        print(f"[db] init_db error: {e}")
        return False


def insert_prediction(jumlah: float, harga: float, pred: float, status: str):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO predictions (jumlah, harga, prediksi_permintaan, status_stok) VALUES (%s,%s,%s,%s)",
            (jumlah, harga, pred, status),
        )
        cur.close()
        conn.close()
        return True
    except Error as e:
        print(f"[db] insert_prediction error: {e}")
        return False


def fetch_history(limit: int = 100):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT id, created_at, jumlah, harga, prediksi_permintaan, status_stok FROM predictions ORDER BY id DESC LIMIT %s",
            (limit,),
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Error as e:
        print(f"[db] fetch_history error: {e}")
        return []


def fetch_history_range(start: str | None = None, end: str | None = None, limit: int = 100):
    """Ambil history dengan filter tanggal opsional.
    start, end format 'YYYY-MM-DD'.
    """
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        where = []
        params = []
        if start:
            where.append("DATE(created_at) >= %s")
            params.append(start)
        if end:
            where.append("DATE(created_at) <= %s")
            params.append(end)
        where_sql = (" WHERE " + " AND ".join(where)) if where else ""
        sql = (
            "SELECT id, created_at, jumlah, harga, prediksi_permintaan, status_stok "
            "FROM predictions" + where_sql + " ORDER BY id DESC LIMIT %s"
        )
        params.append(limit)
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Error as e:
        print(f"[db] fetch_history_range error: {e}")
        return []


def fetch_history_weekly(start: str | None = None, end: str | None = None):
    """Agregasi mingguan menggunakan YEARWEEK ISO (mode 1)."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        where = []
        params = []
        if start:
            where.append("DATE(created_at) >= %s")
            params.append(start)
        if end:
            where.append("DATE(created_at) <= %s")
            params.append(end)
        where_sql = (" WHERE " + " AND ".join(where)) if where else ""
        sql = (
            "SELECT YEARWEEK(created_at, 1) AS yearweek, "
            "MIN(DATE(created_at)) AS week_start, MAX(DATE(created_at)) AS week_end, "
            "AVG(jumlah) AS avg_jumlah, AVG(harga) AS avg_harga, AVG(prediksi_permintaan) AS avg_prediksi, "
            "SUM(jumlah) AS total_jumlah "
            "FROM predictions" + where_sql + " GROUP BY YEARWEEK(created_at,1) ORDER BY week_start ASC"
        )
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Error as e:
        print(f"[db] fetch_history_weekly error: {e}")
        return []


# =========================
#  Stocks helpers (CRUD)
# =========================

def fetch_stocks():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT id, name, qty, unit, updated_at FROM stocks ORDER BY name ASC"
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Error as e:
        print(f"[db] fetch_stocks error: {e}")
        return []


def upsert_stock(name: str, qty: float, unit: str = "kg"):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        # ON DUPLICATE KEY karena name UNIQUE
        cur.execute(
            """
            INSERT INTO stocks (name, qty, unit)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE qty = VALUES(qty), unit = VALUES(unit)
            """,
            (name, qty, unit),
        )
        cur.close()
        conn.close()
        return True
    except Error as e:
        print(f"[db] upsert_stock error: {e}")
        return False


def delete_stock(stock_id: int):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM stocks WHERE id = %s", (stock_id,))
        cur.close()
        conn.close()
        return True
    except Error as e:
        print(f"[db] delete_stock error: {e}")
        return False
