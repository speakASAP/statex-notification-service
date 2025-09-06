# StateX Complete Email System Setup

## 🎯 **What You'll Get**

A **complete professional email system** for StateX with:

### **📧 Email Addresses**
- `contact@statex.cz` - General inquiries
- `admin@statex.cz` - Administrative matters  
- `sales@statex.cz` - Sales inquiries
- `sergej@statex.cz` - Personal contact
- `support@statex.cz` - Technical support

### **🔄 Email Flow**
```
User sends email to contact@statex.cz
           ↓
    StateX Email Server
           ↓
    Forwarded to ssfskype@gmail.com
           ↓
    You receive and can reply
```

### **📤 Sending Emails**
```
StateX Platform sends notification
           ↓
    From: contact@statex.cz
    Reply-To: contact@statex.cz
           ↓
    User receives professional email
```

## 🚀 **Quick Setup (5 Minutes)**

### **Step 1: Start Email Server**
```bash
./setup-email-server.sh
```

### **Step 2: Configure Gmail Forwarding**
1. Go to https://myaccount.google.com/security
2. Enable **2-Factor Authentication**
3. Generate **App Password** for "Mail"
4. Update `email-forwarder/forwarder.py` with your App Password

### **Step 3: Test Email System**
```bash
# Test sending email
python3 test_notifications.py

# Test receiving email (send to contact@statex.cz)
# Check your Gmail for forwarded emails
```

## 🌐 **Access Points**

- **Webmail**: http://localhost:8080 (Roundcube)
- **SMTP**: localhost:587 (for sending)
- **IMAP**: localhost:143 (for receiving)

## 🔧 **Configuration Files**

### **Email Aliases** (`email-config/virtual`)
```
contact@statex.cz    ssfskype@gmail.com
admin@statex.cz      ssfskype@gmail.com
sales@statex.cz      ssfskype@gmail.com
sergej@statex.cz     ssfskype@gmail.com
support@statex.cz    ssfskype@gmail.com
```

### **Notification Service** (`.env`)
```
SMTP_SERVER=email-server
SMTP_PORT=587
SMTP_USERNAME=contact@statex.cz
SMTP_PASSWORD=contact123
SENDER_EMAIL=contact@statex.cz
```

## 📋 **Domain Configuration**

To make this work with your real domain, you need to:

### **1. DNS MX Record**
```
Type: MX
Name: statex.cz
Value: mail.statex.cz
Priority: 10
```

### **2. DNS A Record**
```
Type: A
Name: mail.statex.cz
Value: YOUR_SERVER_IP
```

## 🎯 **Benefits**

- ✅ **Professional**: Emails from your domain
- ✅ **Complete Control**: Your own mail server
- ✅ **Automatic Forwarding**: All emails go to your Gmail
- ✅ **Easy Management**: Web interface available
- ✅ **Scalable**: Handle unlimited emails
- ✅ **Free**: No monthly costs

## 🚀 **Ready to Start?**

Run this command to set up your complete email system:

```bash
./setup-email-server.sh
```

This will give you a **professional email system** that:
1. **Receives** emails at all StateX addresses
2. **Forwards** everything to your Gmail
3. **Sends** professional emails from StateX addresses
4. **Provides** web interface for management

**No monthly fees, complete control, professional setup!** 🎉
