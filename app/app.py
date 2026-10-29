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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)