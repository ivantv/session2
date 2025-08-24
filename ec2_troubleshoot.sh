#!/bin/bash

# EC2 Troubleshooting Script for Flask App
echo "🔍 EC2 Flask App Troubleshooting"
echo "================================"

PORT=6061

echo "1. 🌐 Network Information:"
echo "   Public IP: $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo 'Not available')"
echo "   Private IP: $(curl -s http://169.254.169.254/latest/meta-data/local-ipv4 2>/dev/null || echo 'Not available')"
echo ""

echo "2. 🔌 Port Status:"
echo "   Checking if port $PORT is open..."
if netstat -tuln | grep -q ":$PORT "; then
    echo "   ✅ Port $PORT is listening"
    netstat -tuln | grep ":$PORT "
else
    echo "   ❌ Port $PORT is not listening"
fi
echo ""

echo "3. 🔥 Firewall Status (iptables):"
if command -v iptables &> /dev/null; then
    if iptables -L INPUT -n | grep -q "$PORT"; then
        echo "   ✅ Firewall rules found for port $PORT"
        iptables -L INPUT -n | grep "$PORT"
    else
        echo "   ⚠️  No specific firewall rules for port $PORT"
        echo "   Current INPUT rules:"
        iptables -L INPUT -n | head -10
    fi
else
    echo "   ℹ️  iptables not available"
fi
echo ""

echo "4. 🐍 Python Processes:"
if pgrep -f "python.*app.py" > /dev/null; then
    echo "   ✅ Flask app processes running:"
    ps aux | grep "python.*app.py" | grep -v grep
else
    echo "   ❌ No Flask app processes found"
fi
echo ""

echo "5. 📝 System Logs (last 10 lines):"
if [ -f "/var/log/syslog" ]; then
    echo "   System log:"
    tail -5 /var/log/syslog | grep -i python || echo "   No Python-related logs found"
elif [ -f "/var/log/messages" ]; then
    echo "   System messages:"
    tail -5 /var/log/messages | grep -i python || echo "   No Python-related logs found"
else
    echo "   ℹ️  System logs not accessible"
fi
echo ""

echo "6. 🧪 Testing Local Connection:"
if command -v curl &> /dev/null; then
    echo "   Testing localhost:$PORT..."
    if curl -s --connect-timeout 5 "http://localhost:$PORT" > /dev/null; then
        echo "   ✅ Local connection successful"
    else
        echo "   ❌ Local connection failed"
    fi
else
    echo "   ℹ️  curl not available for testing"
fi
echo ""

echo "7. 🔧 Recommended Actions:"
echo "   • Check AWS Security Group allows inbound TCP $PORT from 0.0.0.0/0"
echo "   • Verify NACL (Network ACL) allows traffic on port $PORT"
echo "   • Ensure Flask app is running with host='0.0.0.0'"
echo "   • Check if any local firewall is blocking the port"
echo "   • Try accessing: http://YOUR_PUBLIC_IP:$PORT"
echo ""

echo "8. 🚀 Quick Start Commands:"
echo "   chmod +x start_production.sh"
echo "   ./start_production.sh"
echo ""

echo "================================"
echo "Troubleshooting complete!"
