from flask import Flask
from flask_cors import CORS
from app.routes import routes
import sys

app = Flask(__name__)
CORS(app)
app.register_blueprint(routes)

if __name__ == "__main__":
    try:
        print("[run] Starting Flask application...")
        print(f"[run] Routes: {len(app.url_map._rules_by_endpoint)}")
        print("[run] Server running on http://0.0.0.0:5000")
        app.run(debug=False, use_reloader=False, host="0.0.0.0", port=5000, threaded=True)
    except KeyboardInterrupt:
        print("\n[run] Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"[run] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
