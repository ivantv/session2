#!/usr/bin/env python3
"""
Simple HTTP Server on port 7070
"""
import http.server
import socketserver
import os
import signal
import sys

PORT = 7070

def signal_handler(sig, frame):
    print('\n🛑 Shutting down HTTP server...')
    sys.exit(0)

def main():
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Change to current directory
    os.chdir('.')
    
    # Create server
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"🌐 Simple HTTP Server started on port {PORT}")
            print(f"📁 Serving files from: {os.getcwd()}")
            print(f"🔗 Access at: http://localhost:{PORT}")
            print(f"🌍 External access: http://0.0.0.0:{PORT}")
            print("⚠️  Press Ctrl+C to stop the server")
            print("-" * 50)
            
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use!")
            print(f"💡 Try: lsof -ti :{PORT} | xargs kill -9")
        else:
            print(f"❌ Error starting server: {e}")
    except KeyboardInterrupt:
        print('\n🛑 Server stopped by user')
    finally:
        print('✅ HTTP server shutdown complete')

if __name__ == '__main__':
    main()

