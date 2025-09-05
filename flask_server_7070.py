#!/usr/bin/env python3
"""
Simple Flask HTTP Server on port 7070
"""
from flask import Flask, send_from_directory, render_template_string
import os
import signal
import sys

app = Flask(__name__)

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple HTTP Server - Port 7070</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .file-list { list-style: none; padding: 0; }
        .file-list li { padding: 8px; border-bottom: 1px solid #eee; }
        .file-list a { text-decoration: none; color: #007bff; }
        .file-list a:hover { text-decoration: underline; }
        .header { background: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 Simple HTTP Server</h1>
            <p><strong>Port:</strong> 7070</p>
            <p><strong>Directory:</strong> {{ directory }}</p>
        </div>
        
        <h2>📁 Files and Directories</h2>
        <ul class="file-list">
            {% for file in files %}
            <li>
                {% if file.is_dir %}
                    📁 <a href="{{ file.name }}/">{{ file.name }}/</a>
                {% else %}
                    📄 <a href="{{ file.name }}">{{ file.name }}</a>
                {% endif %}
            </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """List files in current directory"""
    current_dir = os.getcwd()
    files = []
    
    try:
        for item in sorted(os.listdir('.')):
            if not item.startswith('.'):  # Hide hidden files
                files.append({
                    'name': item,
                    'is_dir': os.path.isdir(item)
                })
    except PermissionError:
        files = [{'name': 'Permission Denied', 'is_dir': False}]
    
    return render_template_string(HTML_TEMPLATE, directory=current_dir, files=files)

@app.route('/<path:filename>')
def serve_file(filename):
    """Serve files from current directory"""
    try:
        return send_from_directory('.', filename)
    except FileNotFoundError:
        return f"File not found: {filename}", 404

def signal_handler(sig, frame):
    print('\n🛑 Shutting down Flask server...')
    sys.exit(0)

if __name__ == '__main__':
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        print('🌐 Simple Flask HTTP Server starting...')
        print(f'📁 Serving files from: {os.getcwd()}')
        print('🔗 Access at: http://localhost:7070')
        print('🌍 External access: http://0.0.0.0:7070')
        print('⚠️  Press Ctrl+C to stop the server')
        print('-' * 50)
        
        app.run(
            host='0.0.0.0',
            port=7070,
            debug=False,
            use_reloader=False
        )
        
    except KeyboardInterrupt:
        print('\n🛑 Server stopped by user')
    except Exception as e:
        print(f'❌ Server error: {e}')
    finally:
        print('✅ Flask server shutdown complete')

