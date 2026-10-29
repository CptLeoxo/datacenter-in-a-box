import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request


app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        dbname=os.environ.get("DB_NAME")
    )


# Root page
@app.route('/')
def home():
    # jsonify for right use for python code
    return jsonify({
        "status": "success",
        "message": "Welcome to Datacenter-in-the-box",
        "service": "Flask App"
    })
    
# /health page
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

# page for status for database
@app.route('/db-check')
def db_check():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "admin"),
            password=os.environ.get("DB_PASSWORD", "secretpassword"),
            dbname=os.environ.get("DB_NAME", "datacenter")
        )

        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()

        cur.close()
        conn.close()


        return jsonify({
            "status": "database connected!",
            "postgres_version": db_version[0]
        }), 200

    except Exception as e:
        return jsonify({"status": "connection failed", "error": str(e)}), 500


@app.route('/setup')
def setup():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            id SERIAL PRIMARY KEY,
            ip_address VARCHAR(45),
            visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "table 'visitors' ready!"})

@app.route('/visit')
def visit():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO visitors (ip_address) VALUES (%s);", (ip,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "recorded", "ip": ip})


@app.route('/visitors')
def visitors():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, ip_address, visit_time FROM visitors ORDER BY visit_time DESC LIMIT 5;")
    records = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(records)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
