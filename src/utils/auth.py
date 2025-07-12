from functools import wraps
from flask import request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

def require_api_key(f):
    """
    Decorator untuk memvalidasi API key
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'API key is required. Please provide X-API-Key header.'
            }), 401
        
        valid_api_key = os.getenv('API_KEY')
        
        if api_key != valid_api_key:
            return jsonify({
                'success': False,
                'error': 'Invalid API key.'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

