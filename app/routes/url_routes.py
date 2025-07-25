from flask import Blueprint, request, jsonify, redirect, abort
from app.models import url_store
from app.utils import is_valid_url, generate_short_code
from datetime import datetime
import threading

url_bp = Blueprint('url_bp', __name__)
lock = threading.Lock()

# Health Check
@url_bp.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@url_bp.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

# Shorten URL
@url_bp.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' field"}), 400

    long_url = data["url"]
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    with lock:
        short_code = generate_short_code()
        while short_code in url_store:
            short_code = generate_short_code()

        url_store[short_code] = {
            "url": long_url,
            "clicks": 0,
            "created_at": datetime.utcnow()
        }

    return jsonify({
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    }), 201

# Redirect
@url_bp.route("/<short_code>", methods=["GET"])
def redirect_short_url(short_code):
    with lock:
        if short_code not in url_store:
            abort(404)

        url_store[short_code]["clicks"] += 1
        return redirect(url_store[short_code]["url"])

# Analytics
@url_bp.route("/api/stats/<short_code>", methods=["GET"])
def stats(short_code):
    with lock:
        if short_code not in url_store:
            return jsonify({"error": "Short code not found"}), 404

        data = url_store[short_code]
        return jsonify({
            "url": data["url"],
            "clicks": data["clicks"],
            "created_at": data["created_at"].isoformat()
        }), 200
