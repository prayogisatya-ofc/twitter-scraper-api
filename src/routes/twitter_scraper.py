from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import asyncio
import random
from datetime import datetime
from src.utils.anti_detection import AntiDetectionUtils, global_rate_limiter
from src.utils.auth import require_api_key
import os
from dotenv import load_dotenv

load_dotenv()

twitter_bp = Blueprint("twitter", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SESSION_FILE = os.path.join(BASE_DIR, "twitter_session.json")

@twitter_bp.route("/scrape", methods=["POST"])
@cross_origin()
@require_api_key
def scrape_tweets():
    """
    Endpoint untuk scraping tweet berdasarkan query search
    
    Request Body:
    {
        "query": "search term"
    }
    
    Response:
    {
        "success": true,
        "data": [
            {
                "username": "user123",
                "content": "tweet content",
                "profile_image": "https://...",
                "created_at": "2024-01-01T12:00:00Z"
            }
        ],
        "count": 20
    }
    """
    try:
        # Cek rate limiting
        if not global_rate_limiter.can_make_request():
            wait_time = global_rate_limiter.wait_time()
            return jsonify({
                "success": False,
                "error": f"Rate limit exceeded. Please wait {wait_time:.1f} seconds.",
                "retry_after": wait_time
            }), 429
        
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({
                "success": False,
                "error": "Query parameter is required"
            }), 400
        
        query = data["query"]
        
        # Validasi query
        if not query.strip():
            return jsonify({
                "success": False,
                "error": "Query cannot be empty"
            }), 400
        
        # Tambahkan request ke rate limiter
        global_rate_limiter.add_request()
        
        # Jalankan scraping
        tweets = asyncio.run(scrape_twitter_data(query))
        
        return jsonify({
            "success": True,
            "data": tweets,
            "count": len(tweets),
            "query": query
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

async def scrape_twitter_data(query):
    """
    Fungsi untuk melakukan scraping data Twitter dengan anti-deteksi
    """
    try:
        # Import twikit di dalam fungsi untuk menghindari error jika belum terinstall
        from twikit import Client
        
        # Inisialisasi client dengan konfigurasi anti-deteksi
        client = Client("en-US")
        
        # 🔁 1. Coba load session dulu
        session_loaded = False
        if os.path.exists(SESSION_FILE):
            try:
                client.load_cookies(SESSION_FILE)
                session_loaded = True
                print("Session loaded")
            except Exception as e:
                print(f"Gagal load session: {e}")

        # 🔍 2. Coba scraping dengan session
        if session_loaded:
            try:
                tweets = await client.search_tweet(
                    query=query,
                    product="Latest",
                    count=20
                )
            except Exception as e:
                print(f"Session kadaluarsa atau tidak valid: {e}")
                session_loaded = False  # tandai untuk login ulang

        # 🔐 3. Login jika session gagal atau tidak tersedia
        if not session_loaded:
            await AntiDetectionUtils.random_delay(2, 5)
            try:
                await client.login(
                    auth_info_1=os.getenv("TWITTER_USERNAME"),
                    auth_info_2=os.getenv("TWITTER_EMAIL"),
                    password=os.getenv("TWITTER_PASSWORD")
                )
                await AntiDetectionUtils.random_delay(1, 3)
                print("Login berhasil")

                # Simpan session baru
                client.save_cookies(SESSION_FILE)
                print("Session disimpan")

                tweets = await client.search_tweet(
                    query=query,
                    product="Latest",
                    count=20
                )
            except Exception as login_err:
                print(f"Gagal login: {login_err}")
                # Return empty list on login failure instead of fallback
                return []
        
        # Extract data yang dibutuhkan dengan error handling
        result = []
        for tweet in tweets:
            try:
                # print(vars(tweet))
                # Delay kecil antar processing tweet
                await asyncio.sleep(random.uniform(0.1, 0.3))
                
                tweet_data = {
                    "username": getattr(tweet.user, "screen_name", "unknown"),
                    "content": getattr(tweet, "text", ""),
                    "profile_image": getattr(tweet.user, "profile_image_url", ""),
                    "created_at": getattr(tweet, "created_at", datetime.now().isoformat())
                }
                result.append(tweet_data)
                
                # Batasi hasil maksimal 20
                if len(result) >= 20:
                    break
                    
            except Exception as e:
                # Skip tweet yang error dan lanjutkan
                continue
        
        return result
        
    except ImportError:
        # Fallback jika twikit tidak tersedia, return empty list
        print("Twikit not available. Returning empty data.")
        return []
    except Exception as e:
        # Fallback jika twikit gagal, return empty list
        print(f"Twikit error: {str(e)}. Returning empty data.")
        return []

# Remove scrape_twitter_fallback function as it's no longer needed

@twitter_bp.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        "status": "healthy",
        "service": "Twitter Scraper API",
        "timestamp": datetime.now().isoformat()
    })

@twitter_bp.route("/rate-limit-status", methods=["GET"])
def rate_limit_status():
    """
    Endpoint untuk mengecek status rate limiting
    """
    can_request = global_rate_limiter.can_make_request()
    wait_time = global_rate_limiter.wait_time() if not can_request else 0
    
    return jsonify({
        "can_make_request": can_request,
        "wait_time": wait_time,
        "requests_made": len(global_rate_limiter.requests),
        "max_requests": global_rate_limiter.max_requests,
        "time_window": global_rate_limiter.time_window
    })


