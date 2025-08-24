#!/usr/bin/env python3
"""
Enhanced Flask application runner with proper port management
"""
import os
import sys
import signal
import socket
import subprocess
from app import app

def check_port_available(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False

def kill_processes_on_port(port):
    """Kill processes using the specified port"""
    try:
        # Find processes using the port
        result = subprocess.run(['lsof', '-ti', f':{port}'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    print(f"🔄 Killing process {pid} on port {port}")
                    subprocess.run(['kill', '-9', pid])
            return True
    except Exception as e:
        print(f"⚠️  Could not kill processes on port {port}: {e}")
    return False

def graceful_shutdown(signum, frame):
    """Handle graceful shutdown"""
    print('\n🛑 Shutting down Flask application gracefully...')
    sys.exit(0)

def main():
    port = 6061
    
    # Register signal handlers
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)
    
    # Check if port is available
    if not check_port_available(port):
        print(f"⚠️  Port {port} is in use. Attempting to free it...")
        if kill_processes_on_port(port):
            print(f"✅ Port {port} freed successfully")
        else:
            print(f"❌ Could not free port {port}. Trying a different port...")
            port = 6062  # Try next port
    
    try:
        print('🚀 Starting Organic Chemistry 3D Flask Application')
        print(f'🌐 Server running on: http://localhost:{port}')
        print('📚 Browse 3D molecular structures')
        print('🧪 Take interactive quizzes')
        print('⚠️  Press Ctrl+C to stop the server')
        print('-' * 50)
        
        app.run(
            debug=True,
            host='0.0.0.0',
            port=port,
            use_reloader=False,  # Disable reloader to prevent multiple processes
            threaded=True
        )
        
    except KeyboardInterrupt:
        print('\n🛑 Server stopped by user')
    except Exception as e:
        print(f'\n❌ Server error: {e}')
    finally:
        print('✅ Flask application shutdown complete')
        print('🔄 Port should now be available for reuse')

if __name__ == '__main__':
    main()
