#!/usr/bin/env python3
"""
Quote of the Day - 3-Tier Application
Presentation Tier: Flask web application serving HTML/CSS/JavaScript
Application Tier: Flask REST API with business logic
Data Tier: PostgreSQL database with quotes, authors, votes
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2
import psycopg2.extras
import os
import random
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Database configuration from environment variables
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', '3-tier-app-example-db')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', 'postgres')

def get_db_connection(max_retries=5, retry_delay=2):
    """Get database connection with retry logic."""
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting database connection (attempt {attempt + 1}/{max_retries})")
            logger.info(f"Connecting to: host={DB_HOST}, port={DB_PORT}, database={DB_NAME}, user={DB_USER}")
            
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                cursor_factory=psycopg2.extras.RealDictCursor,
                connect_timeout=10
            )
            logger.info("Database connection successful!")
            return conn
            
        except Exception as e:
            logger.error(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("All database connection attempts failed")
                return None

def init_database():
    """Initialize database with tables and sample data."""
    logger.info("Starting database initialization...")
    
    # Wait for database to be ready
    logger.info("Waiting for database connection...")
    conn = None
    for attempt in range(30):  # Wait up to 60 seconds
        conn = get_db_connection()
        if conn:
            break
        logger.info(f"Database not ready, attempt {attempt + 1}/30, waiting 2 seconds...")
        time.sleep(2)
    
    if not conn:
        logger.error("Cannot initialize database - no connection after 30 attempts")
        return False
    
    try:
        cursor = conn.cursor()
        logger.info("Creating database tables...")
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                bio TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        logger.info("Authors table created/verified")
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id SERIAL PRIMARY KEY,
                author_id INTEGER REFERENCES authors(id),
                text TEXT NOT NULL,
                category VARCHAR(50) DEFAULT 'wisdom',
                upvotes INTEGER DEFAULT 0,
                downvotes INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        logger.info("Quotes table created/verified")
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_votes (
                id SERIAL PRIMARY KEY,
                quote_id INTEGER REFERENCES quotes(id),
                user_ip VARCHAR(45),
                vote_type VARCHAR(10) CHECK (vote_type IN ('up', 'down')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(quote_id, user_ip)
            );
        ''')
        logger.info("User_votes table created/verified")
        
        # Check if sample data exists
        cursor.execute("SELECT COUNT(*) FROM authors;")
        author_count = cursor.fetchone()['count']
        logger.info(f"Found {author_count} authors in database")
        
        if author_count == 0:
            logger.info("Inserting sample data...")
            # Insert sample authors
            sample_authors = [
                ("Albert Einstein", "Theoretical physicist known for the theory of relativity"),
                ("Maya Angelou", "American poet, memoirist, and civil rights activist"),
                ("Steve Jobs", "Co-founder of Apple Inc."),
                ("Nelson Mandela", "South African anti-apartheid leader and former president"),
                ("Marie Curie", "Polish-French physicist and chemist"),
                ("Mark Twain", "American writer and humorist"),
                ("Oprah Winfrey", "American media executive and philanthropist")
            ]
            
            for name, bio in sample_authors:
                cursor.execute(
                    "INSERT INTO authors (name, bio) VALUES (%s, %s);",
                    (name, bio)
                )
            logger.info(f"Inserted {len(sample_authors)} authors")
            
            # Insert sample quotes
            sample_quotes = [
                (1, "Imagination is more important than knowledge.", "wisdom"),
                (1, "Try not to become a person of success, but rather try to become a person of value.", "success"),
                (2, "If you don't like something, change it. If you can't change it, change your attitude.", "attitude"),
                (2, "I've learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel.", "relationships"),
                (3, "Innovation distinguishes between a leader and a follower.", "innovation"),
                (3, "Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work.", "work"),
                (4, "It always seems impossible until it's done.", "perseverance"),
                (4, "Education is the most powerful weapon which you can use to change the world.", "education"),
                (5, "Nothing in life is to be feared, it is only to be understood.", "knowledge"),
                (6, "The secret of getting ahead is getting started.", "motivation"),
                (7, "The biggest adventure you can take is to live the life of your dreams.", "dreams")
            ]
            
            for author_id, text, category in sample_quotes:
                cursor.execute(
                    "INSERT INTO quotes (author_id, text, category) VALUES (%s, %s, %s);",
                    (author_id, text, category)
                )
            logger.info(f"Inserted {len(sample_quotes)} quotes")
        else:
            logger.info("Sample data already exists, skipping insertion")
        
        conn.commit()
        logger.info("Database initialized successfully!")
        return True
        
    except Exception as e:
        conn.rollback()
        logger.error(f"Database initialization failed: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# PRESENTATION TIER - Web Pages
@app.route('/')
def index():
    """Home page showing quote of the day."""
    return render_template('index.html')

@app.route('/browse')
def browse():
    """Browse all quotes by category."""
    return render_template('browse.html')

@app.route('/authors')
def authors():
    """Authors page."""
    return render_template('authors.html')

# APPLICATION TIER - REST API Endpoints
@app.route('/api/quote-of-the-day')
def api_quote_of_the_day():
    """Get a random quote for the day."""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT q.id, q.text, q.category, q.upvotes, q.downvotes,
                   a.name as author_name, a.bio as author_bio
            FROM quotes q
            JOIN authors a ON q.author_id = a.id
            ORDER BY RANDOM()
            LIMIT 1;
        ''')
        
        quote = cursor.fetchone()
        if quote:
            return jsonify(dict(quote))
        else:
            return jsonify({'error': 'No quotes found'}), 404
            
    except Exception as e:
        logger.error(f"Error fetching quote: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/quotes')
def api_quotes():
    """Get all quotes with optional category filter."""
    category = request.args.get('category')
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        if category:
            cursor.execute('''
                SELECT q.id, q.text, q.category, q.upvotes, q.downvotes,
                       a.name as author_name
                FROM quotes q
                JOIN authors a ON q.author_id = a.id
                WHERE q.category = %s
                ORDER BY (q.upvotes - q.downvotes) DESC;
            ''', (category,))
        else:
            cursor.execute('''
                SELECT q.id, q.text, q.category, q.upvotes, q.downvotes,
                       a.name as author_name
                FROM quotes q
                JOIN authors a ON q.author_id = a.id
                ORDER BY (q.upvotes - q.downvotes) DESC;
            ''')
        
        quotes = cursor.fetchall()
        return jsonify([dict(quote) for quote in quotes])
        
    except Exception as e:
        logger.error(f"Error fetching quotes: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/authors')
def api_authors():
    """Get all authors with their quote counts."""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.name, a.bio,
                   COUNT(q.id) as quote_count
            FROM authors a
            LEFT JOIN quotes q ON a.id = q.author_id
            GROUP BY a.id, a.name, a.bio
            ORDER BY quote_count DESC;
        ''')
        
        authors = cursor.fetchall()
        return jsonify([dict(author) for author in authors])
        
    except Exception as e:
        logger.error(f"Error fetching authors: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/vote', methods=['POST'])
def api_vote():
    """Vote on a quote (up or down)."""
    data = request.get_json()
    quote_id = data.get('quote_id')
    vote_type = data.get('vote_type')  # 'up' or 'down'
    user_ip = request.remote_addr
    
    if not quote_id or vote_type not in ['up', 'down']:
        return jsonify({'error': 'Invalid vote data'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        
        # Check if user already voted
        cursor.execute(
            "SELECT vote_type FROM user_votes WHERE quote_id = %s AND user_ip = %s;",
            (quote_id, user_ip)
        )
        existing_vote = cursor.fetchone()
        
        if existing_vote:
            # Update existing vote
            old_vote = existing_vote['vote_type']
            if old_vote != vote_type:
                # Remove old vote and add new vote
                if old_vote == 'up':
                    cursor.execute("UPDATE quotes SET upvotes = upvotes - 1 WHERE id = %s;", (quote_id,))
                else:
                    cursor.execute("UPDATE quotes SET downvotes = downvotes - 1 WHERE id = %s;", (quote_id,))
                
                # Add new vote
                if vote_type == 'up':
                    cursor.execute("UPDATE quotes SET upvotes = upvotes + 1 WHERE id = %s;", (quote_id,))
                else:
                    cursor.execute("UPDATE quotes SET downvotes = downvotes + 1 WHERE id = %s;", (quote_id,))
                
                # Update vote record
                cursor.execute(
                    "UPDATE user_votes SET vote_type = %s, created_at = CURRENT_TIMESTAMP WHERE quote_id = %s AND user_ip = %s;",
                    (vote_type, quote_id, user_ip)
                )
                
                conn.commit()
                return jsonify({'success': True, 'message': 'Vote updated'})
            else:
                return jsonify({'success': True, 'message': 'Vote already exists'})
        else:
            # New vote
            cursor.execute(
                "INSERT INTO user_votes (quote_id, user_ip, vote_type) VALUES (%s, %s, %s);",
                (quote_id, user_ip, vote_type)
            )
            
            if vote_type == 'up':
                cursor.execute("UPDATE quotes SET upvotes = upvotes + 1 WHERE id = %s;", (quote_id,))
            else:
                cursor.execute("UPDATE quotes SET downvotes = downvotes + 1 WHERE id = %s;", (quote_id,))
            
            conn.commit()
            return jsonify({'success': True, 'message': 'Vote recorded'})
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Error recording vote: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/health')
def health_check():
    """Health check endpoint for load balancer."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            cursor.fetchone()
            cursor.close()
            conn.close()
            return jsonify({
                'status': 'healthy', 
                'timestamp': datetime.now().isoformat(),
                'database': 'connected'
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy', 
                'error': f'database query failed: {e}',
                'timestamp': datetime.now().isoformat()
            }), 503
    else:
        return jsonify({
            'status': 'unhealthy', 
            'error': 'database connection failed',
            'timestamp': datetime.now().isoformat()
        }), 503

@app.route('/api/debug')
def debug_info():
    """Debug endpoint to check database connection details."""
    return jsonify({
        'db_host': DB_HOST,
        'db_port': DB_PORT,
        'db_name': DB_NAME,
        'db_user': DB_USER,
        'environment_vars': dict(os.environ),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    logger.info("Starting Quote of the Day application...")
    
    # Initialize database
    if init_database():
        logger.info("Database ready!")
    else:
        logger.error("Database initialization failed!")
    
    # Start the Flask application
    app.run(host='0.0.0.0', port=80, debug=False)
