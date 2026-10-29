import os
import psycopg2
from flask import Flask, jsonify


app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
