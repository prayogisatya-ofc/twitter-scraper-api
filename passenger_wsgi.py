
#!/usr/bin/env python3
"""
Passenger WSGI entry point
File ini digunakan untuk hosting yang menggunakan Passenger (seperti cPanel)
"""

import sys
import os

# Tambahkan path project ke sys.path
project_path = os.path.dirname(os.path.abspath(__file__))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Aktifkan virtual environment jika ada
venv_path = os.path.join(project_path, 'venv', 'lib', 'python3.11', 'site-packages')
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)

# Import aplikasi Flask
try:
    from src.main import app
    application = app
except ImportError as e:
    # Fallback jika import gagal
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [f'Import Error: {str(e)}'.encode('utf-8')]

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=False)


