#!/usr/bin/env python3
"""
Database connection test script for Quote of the Day application
"""

import psycopg2
import psycopg2.extras
import os
import sys
import time

# Database configuration
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', '3-tier-app-example-db')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', 'postgres')

def test_connection():
    """Test database connection."""
    print("🔍 Testing database connection...")
    print(f"   Host: {DB_HOST}")
    print(f"   Port: {DB_PORT}")
    print(f"   Database: {DB_NAME}")
    print(f"   User: {DB_USER}")
    print()
    
    try:
        print("📡 Attempting to connect...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            cursor_factory=psycopg2.extras.RealDictCursor,
            connect_timeout=10
        )
        
        print("✅ Connection successful!")
        
        # Test basic query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"📊 PostgreSQL version: {version['version']}")
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()
        print(f"📋 Tables found: {[table['table_name'] for table in tables]}")
        
        # Check data counts
        try:
            cursor.execute("SELECT COUNT(*) as count FROM authors;")
            author_count = cursor.fetchone()['count']
            print(f"👥 Authors: {author_count}")
            
            cursor.execute("SELECT COUNT(*) as count FROM quotes;")
            quote_count = cursor.fetchone()['count']
            print(f"💬 Quotes: {quote_count}")
            
            cursor.execute("SELECT COUNT(*) as count FROM user_votes;")
            vote_count = cursor.fetchone()['count']
            print(f"🗳️  Votes: {vote_count}")
            
        except Exception as e:
            print(f"⚠️  Tables might not exist yet: {e}")
        
        cursor.close()
        conn.close()
        print("\n🎉 Database connection test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def main():
    """Main function."""
    print("=" * 60)
    print("🧪 Quote of the Day - Database Connection Test")
    print("=" * 60)
    
    if test_connection():
        sys.exit(0)
    else:
        print("\n🚨 Database connection test FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
