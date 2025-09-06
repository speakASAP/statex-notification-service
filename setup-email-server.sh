#!/bin/bash

# StateX Email Server Setup Script

echo "🚀 Setting up StateX Email Server..."

# Create SSL certificates
echo "📜 Creating SSL certificates..."
openssl req -x509 -newkey rsa:4096 -keyout email-ssl/statex.key -out email-ssl/statex.crt -days 365 -nodes -subj "/C=CZ/ST=Prague/L=Prague/O=StateX/OU=IT/CN=mail.statex.cz"

# Set permissions
chmod 600 email-ssl/statex.key
chmod 644 email-ssl/statex.crt

# Create virtual aliases database
echo "📧 Setting up email aliases..."
postmap email-config/virtual

# Create mail directories
echo "📁 Creating mail directories..."
mkdir -p email-data/statex
chmod 755 email-data/statex

# Start email server
echo "🚀 Starting email server..."
docker compose -f docker-compose.email-complete.yml up -d

echo "✅ StateX Email Server is running!"
echo ""
echo "📧 Email addresses configured:"
echo "   - contact@statex.cz → ssfskype@gmail.com"
echo "   - admin@statex.cz → ssfskype@gmail.com"
echo "   - sales@statex.cz → ssfskype@gmail.com"
echo "   - sergej@statex.cz → ssfskype@gmail.com"
echo "   - support@statex.cz → ssfskype@gmail.com"
echo ""
echo "🌐 Webmail interface: http://localhost:8080"
echo "📧 SMTP server: localhost:587"
echo "📥 IMAP server: localhost:143"
echo ""
echo "🔧 Next steps:"
echo "1. Configure your domain's MX records to point to this server"
echo "2. Test email sending and receiving"
echo "3. Set up Gmail App Password for forwarding"
