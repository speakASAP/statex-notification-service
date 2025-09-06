# StateX Notification Service

A dedicated microservice for handling notifications across multiple channels (Email, WhatsApp, Telegram) for the StateX platform.

## 🚀 Features

- **Multi-Channel Support**: Email, WhatsApp, Telegram
- **Professional Templates**: Beautiful HTML email templates
- **Scalable Architecture**: Built with FastAPI and Docker
- **Real-time Notifications**: Instant delivery across all channels
- **Comprehensive Logging**: Full notification tracking and statistics
- **Easy Integration**: Simple REST API for other services

## 📋 Supported Channels

| Channel | Status | Configuration Required |
|---------|--------|----------------------|
| 📧 Email (SMTP) | ✅ Ready | SMTP credentials |
| 📱 WhatsApp | ✅ Ready | WhatsApp Business API |
| ✈️ Telegram | ✅ Ready | Telegram Bot API |

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   StateX        │    │   Notification   │    │   External      │
│   Platform      │───▶│   Service        │───▶│   APIs          │
│                 │    │                  │    │                 │
│ - User Portal   │    │ - Email SMTP     │    │ - StateX Mailserver │
│ - Form Service  │    │ - WhatsApp API   │    │ - WhatsApp      │
│ - AI Service    │    │ - Telegram API   │    │ - Telegram      │
└─────────────────┘                           └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)

### Running with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/speakASAP/statex-notification-service.git
   cd statex-notification-service
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Start the service**
   ```bash
   docker compose up -d
   ```

4. **Test the service**
   ```bash
   curl http://localhost:8005/health
   ```

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**
   ```bash
   export SMTP_USERNAME="your-email@gmail.com"
   export SMTP_PASSWORD="your-app-password"
   # ... other credentials
   ```

3. **Run the service**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
   ```

## 📡 API Documentation

### Send Notification
```http
POST /api/notifications
Content-Type: application/json

{
  "user_id": "user-123",
  "type": "confirmation",
  "title": "Form Submission Confirmed",
  "message": "Thank you for your submission!",
  "contact_type": "email",
  "contact_value": "user@example.com",
  "user_name": "John Doe"
}
```

### Get Notifications
```http
GET /api/notifications
```

### Get Statistics
```http
GET /api/notifications/stats
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SMTP_SERVER` | StateX mailserver hostname | Yes (for email) |
| `SMTP_PORT` | StateX mailserver port | Yes (for email) |
| `SMTP_USERNAME` | StateX email username | Yes (for email) |
| `SMTP_PASSWORD` | StateX email password | Yes (for email) |
| `SENDER_EMAIL` | From email address | Yes (for email) |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | Yes (for Telegram) |
| `TELEGRAM_CHAT_ID` | Telegram chat ID | Yes (for Telegram) |
| `WHATSAPP_ACCESS_TOKEN` | WhatsApp access token | Yes (for WhatsApp) |
| `WHATSAPP_PHONE_NUMBER_ID` | WhatsApp phone number ID | Yes (for WhatsApp) |

## 🧪 Testing

### Test Script
```bash
python test_notifications.py
```

### Manual Testing
```bash
# Test email notification
curl -X POST http://localhost:8005/api/notifications \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "type": "confirmation",
    "title": "Test Email",
    "message": "This is a test notification",
    "contact_type": "email",
    "contact_value": "test@example.com",
    "user_name": "Test User"
  }'
```

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8005/health
```

### Statistics
```bash
curl http://localhost:8005/api/notifications/stats
```

## 🚀 Deployment

### Docker
```bash
docker build -t statex-notification-service .
docker run -p 8005:8005 --env-file .env statex-notification-service
```

### Docker Compose
```bash
docker compose up -d
```

### Kubernetes
```bash
kubectl apply -f k8s/
```

## 🔒 Security

- All credentials stored as environment variables
- No hardcoded secrets in code
- HTTPS support for production
- Rate limiting (configurable)
- Input validation and sanitization

## 📈 Performance

- Async/await for non-blocking operations
- Connection pooling for external APIs
- Retry logic with exponential backoff
- Comprehensive error handling
- Request/response logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in this repository
- Contact the StateX team
- Check the documentation

## 🔄 Changelog

### v1.0.0
- Initial release
- Multi-channel notification support
- Docker containerization
- Comprehensive API documentation
