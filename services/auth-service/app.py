from flask import Flask, request, jsonify
import jwt
import datetime
import os

app = Flask(__name__)

# Secret used to sign JWT tokens
SECRET_KEY = os.getenv("AUTH_SECRET", "supersecret123")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "service": "auth-service",
        "status": "ok"
    }), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    
    username = data.get("username")
    password = data.get("password")

    # --- Simple authentication logic (for project demo) ---
    if username == "admin" and password == "password":
        token = jwt.encode(
            {
                "username": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                "iat": datetime.datetime.utcnow()
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({"token": token}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/validate", methods=["POST"])
def validate_token():
    data = request.get_json() or {}
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token missing"}), 400

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"valid": True, "data": decoded}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"valid": False, "error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"valid": False, "error": "Invalid token"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
