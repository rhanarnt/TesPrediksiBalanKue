#!/usr/bin/env python
"""Test Flask app startup"""
import traceback
import sys

try:
    print("=" * 60)
    print("Starting Flask app test...")
    print("=" * 60)
    
    from run import app
    print("OK: Flask app imported successfully")
    print(f"OK: Routes registered: {len(app.url_map._rules_by_endpoint)}")
    
    print("\n" + "=" * 60)
    print("Running development server...")
    print("=" * 60)
    app.run(debug=False, use_reloader=False, host="0.0.0.0", port=5000)
    
except Exception as e:
    print(f"\nERROR: {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
