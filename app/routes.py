from flask import Blueprint, request, jsonify, send_from_directory, render_template, Response
import joblib
import numpy as np
import os
from .db import (
    init_db,
    insert_prediction,
    fetch_history,
    fetch_history_range,
    fetch_history_weekly,
    fetch_stocks,
    upsert_stock,
    delete_stock,
)
from .auth import (
    ensure_users_table,
    authenticate_user,
    generate_jwt_token,
    require_auth,
)

routes = Blueprint("routes", __name__)

# load model (nanti kamu harus training dulu pakai models.py)
try:
    lr = joblib.load("app/lr_model.pkl")
    rf = joblib.load("app/rf_model.pkl")
except:
    lr, rf = None, None

@routes.route("/")
def home():
    return {"message": "API Prediksi Stok Kue siap digunakan"}


# ============================
#   Authentication Routes
# ============================

@routes.route("/login", methods=["POST"])
def login():
    """
    Login endpoint - authenticate user and return JWT token
    """
    try:
        # Ensure users table exists
        try:
            ensure_users_table()
        except Exception as e:
            print(f"[login] Failed to ensure users table: {e}")
            return {"error": "Database error", "detail": str(e)}, 500

        # Validasi content type
        if not request.is_json:
            return {"error": "Content-Type harus application/json"}, 400

        data = request.get_json(silent=True)
        if data is None:
            return {"error": "Body JSON tidak valid"}, 400

        # Validasi field
        email = (data.get("email") or "").strip()
        password = data.get("password") or ""

        if not email or not password:
            return {"error": "Email dan password wajib"}, 400

        if "@" not in email or "." not in email:
            return {"error": "Format email tidak valid"}, 400

        # Authenticate
        user = authenticate_user(email, password)
        if not user:
            print(f"[login] Authentication failed for email: {email}")
            return {"error": "Email atau password salah"}, 401

        # Generate token
        token = generate_jwt_token(user["id"], user["email"])
        print(f"[login] Authentication successful for: {email}")
        return {
            "token": token,
            "user": user,
        }, 200
    
    except Exception as e:
        print(f"[login] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return {"error": f"Internal server error: {str(e)}"}, 500


@routes.route("/health")
def health():
    status = {
        "status": "ok",
        "model_regression": bool(lr),
        "model_classifier": bool(rf)
    }
    return jsonify(status)


@routes.route("/app")
def app_page():
    # Sajikan file test.html dari root proyek agar mudah diakses dari mobile
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    # project_root sekarang menunjuk ke folder root proyek (yang berisi test.html)
    return send_from_directory(project_root, "test.html")

@routes.route("/manifest.webmanifest")
def manifest():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return send_from_directory(project_root, "manifest.webmanifest")

@routes.route("/sw.js")
def service_worker():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    # service worker harus diserve dengan mime type js
    response = send_from_directory(project_root, "sw.js")
    response.headers["Content-Type"] = "application/javascript"
    return response

@routes.route("/offline.html")
def offline_page():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return send_from_directory(project_root, "offline.html")

@routes.route("/init-db")
def init_db_route():
    ok = init_db()
    return ({"status": "ok"} if ok else {"status": "error"}), (200 if ok else 500)


@routes.route("/history")
def history():
    start = request.args.get("start")
    end = request.args.get("end")
    limit = int(request.args.get("limit", 100))
    if start or end:
        rows = fetch_history_range(start=start, end=end, limit=limit)
    else:
        rows = fetch_history(limit=limit)
    return jsonify(rows)

@routes.route("/history/weekly")
def history_weekly():
    start = request.args.get("start")
    end = request.args.get("end")
    rows = fetch_history_weekly(start=start, end=end)
    return jsonify(rows)

@routes.route("/history.csv")
def history_csv():
    start = request.args.get("start")
    end = request.args.get("end")
    limit = int(request.args.get("limit", 1000))
    rows = fetch_history_range(start=start, end=end, limit=limit) if (start or end) else fetch_history(limit=limit)
    # Build CSV
    header = ["id","created_at","jumlah","harga","prediksi_permintaan","status_stok"]
    def to_lines():
        yield ",".join(header) + "\n"
        for r in rows:
            vals = [str(r.get(k, "")) for k in header]
            yield ",".join(vals) + "\n"
    return Response(to_lines(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=history.csv"})

@routes.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@routes.route("/prediksi", methods=["POST"])
def prediksi():
    # Pastikan model sudah tersedia
    if not lr or not rf:
        return {"error": "Model belum dilatih. Jalankan training di models.py"}, 400

    # Validasi content-type dan body JSON
    if not request.is_json:
        return {"error": "Content-Type harus application/json"}, 400

    data = request.get_json(silent=True)
    if data is None:
        return {"error": "Body JSON tidak valid"}, 400

    # Cek field wajib
    missing = [k for k in ("jumlah", "harga") if k not in data]
    if missing:
        return {"error": "Field wajib tidak lengkap", "missing": missing}, 400

    # Konversi ke numerik dan validasi nilai
    try:
        jumlah = float(data.get("jumlah"))
    except Exception:
        return {"error": "Field 'jumlah' harus numerik"}, 400

    try:
        harga = float(data.get("harga"))
    except Exception:
        return {"error": "Field 'harga' harus numerik"}, 400

    if not (np.isfinite(jumlah) and np.isfinite(harga)):
        return {"error": "Nilai 'jumlah' dan 'harga' harus angka hingga (bukan NaN/Inf)"}, 400

    # Logging ringan input yang valid
    try:
        print(f"[prediksi] input -> jumlah={jumlah}, harga={harga}")
    except Exception:
        pass

    # Prediksi dengan penanganan error terkontrol
    try:
        X = np.array([[jumlah, harga]])
        prediksi_permintaan = lr.predict(X)[0]
        status_stok = rf.predict(X)[0]
    except Exception as e:
        return {"error": "Gagal melakukan prediksi", "detail": str(e)}, 500

    # Logging ringan hasil prediksi
    try:
        print(f"[prediksi] output -> permintaan={float(prediksi_permintaan)}, status={str(status_stok)}")
    except Exception:
        pass

    # Simpan ke database (opsional, jika koneksi tersedia)
    try:
        insert_prediction(jumlah, harga, float(prediksi_permintaan), str(status_stok))
    except Exception as e:
        print(f"[prediksi] gagal simpan DB: {e}")

    return jsonify({
        "prediksi_permintaan": float(prediksi_permintaan),
        "status_stok": str(status_stok)
    })


# Alias untuk integrasi Flutter (konsisten dengan dokumen): /predict
@routes.route("/predict", methods=["POST"])
def predict_alias():
    return prediksi()


# =========================
#   Stock Management API
# =========================

@routes.route("/stock", methods=["GET"])
def stock_list():
    rows = fetch_stocks()
    return jsonify(rows)


@routes.route("/stock", methods=["POST"])
def stock_upsert():
    if not request.is_json:
        return {"error": "Content-Type harus application/json"}, 400
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    if not name:
        return {"error": "Field 'name' wajib"}, 400

    try:
        qty = float(data.get("qty", 0))
    except Exception:
        return {"error": "Field 'qty' harus numerik"}, 400

    unit = (str(data.get("unit")) if data.get("unit") else "kg").strip() or "kg"

    ok = upsert_stock(name=name, qty=qty, unit=unit)
    if not ok:
        return {"status": "error"}, 500
    return {"status": "ok"}


@routes.route("/stock/<int:stock_id>", methods=["DELETE"])
def stock_delete(stock_id: int):
    ok = delete_stock(stock_id)
    if not ok:
        return {"status": "error"}, 500
    return {"status": "ok"}
