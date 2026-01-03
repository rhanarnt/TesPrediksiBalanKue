#!/usr/bin/env python
"""
Create database in MySQL Laragon before running init_db.py
"""

try:
    import pymysql
except ImportError:
    print("❌ Error: pymysql tidak terinstall")
    print("   Install dengan: pip install PyMySQL")
    exit(1)

import sys

def create_database():
    """Create database if it doesn't exist"""
    print("\n" + "="*60)
    print("🎂 Creating MySQL Database")
    print("="*60 + "\n")
    
    try:
        # Connect to MySQL server without specifying database
        connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("✅ Connected to MySQL server")
        
        cursor = connection.cursor()
        
        # Create database
        print("📦 Creating database 'prediksi_stok_kue'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS prediksi_stok_kue CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        connection.commit()
        
        print("✅ Database created successfully")
        print("\n" + "="*60)
        print("Next steps:")
        print("  1. Run: python init_db.py")
        print("  2. Then: python run.py")
        print("="*60 + "\n")
        
        cursor.close()
        connection.close()
        
        return 0
        
    except pymysql.Error as e:
        print(f"❌ MySQL Error: {e}")
        print("\n⚠️  Make sure:")
        print("   1. Laragon is running")
        print("   2. MySQL is active in Laragon")
        print("   3. MySQL is running on 127.0.0.1:3306")
        print("="*60 + "\n")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(create_database())
