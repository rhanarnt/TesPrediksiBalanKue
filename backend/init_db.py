#!/usr/bin/env python
"""
Database initialization script for BakeSmart
Run this after setting up MySQL in Laragon
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from database import db, init_db, seed_db

def main():
    """Initialize database"""
    print("\n" + "="*60)
    print("🎂 BakeSmart Database Initialization")
    print("="*60 + "\n")
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'mysql+pymysql://root:@127.0.0.1:3306/prediksi_stok_kue'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        try:
            print("📊 Connecting to MySQL database...")
            print(f"   URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Create all tables
            print("🔨 Creating database tables...")
            init_db(app)
            
            # Seed initial data
            print("🌱 Seeding initial data...")
            seed_db(app)
            
            print("\n" + "="*60)
            print("✅ Database initialization completed successfully!")
            print("="*60)
            print("\n📝 Default Credentials:")
            print("   Email: admin@bakesmart.com")
            print("   Password: admin123")
            print("\n🚀 Now run: python run.py")
            print("="*60 + "\n")
            
        except Exception as e:
            print("\n" + "="*60)
            print(f"❌ Error: {str(e)}")
            print("="*60)
            print("\n⚠️  Troubleshooting:")
            print("   1. Check if Laragon MySQL is running")
            print("   2. Verify DATABASE_URL in .env")
            print("   3. Create database: mysql -u root -e \"CREATE DATABASE prediksi_stok_kue;\"")
            print("="*60 + "\n")
            return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
