# StateX Email Server Setup

## 🎯 **Goal**: Professional Email System for StateX

We need to set up email sending capabilities for these StateX email addresses:
- `contact@statex.cz` - General inquiries
- `admin@statex.cz` - Administrative matters  
- `sales@statex.cz` - Sales inquiries
- `sergej@statex.cz` - Personal contact
- `support@statex.cz` - Technical support

## 🚀 **Recommended Approach: Professional Email Service**

Instead of running our own mail server (complex, maintenance-heavy), let's use a professional email service:

### **Option 1: Mailgun (Recommended)**
- **Pros**: Reliable, professional, easy setup, good deliverability
- **Cost**: Free tier (10,000 emails/month)
- **Setup**: 15 minutes

### **Option 2: SendGrid**
- **Pros**: Very reliable, excellent deliverability
- **Cost**: Free tier (100 emails/day)
- **Setup**: 20 minutes

### **Option 3: AWS SES**
- **Pros**: Very cheap, scalable
- **Cost**: $0.10 per 1,000 emails
- **Setup**: 30 minutes

## 📧 **Email Configuration for Notification Service**

### **Mailgun Setup (Recommended)**

1. **Sign up at Mailgun** (https://mailgun.com)
2. **Verify your domain** `statex.cz`
3. **Get API credentials**:
   ```bash
   MAILGUN_API_KEY=your-mailgun-api-key
   MAILGUN_DOMAIN=statex.cz
   ```

4. **Configure notification service**:
   ```bash
   # In .env file
   SMTP_SERVER=smtp.mailgun.org
   SMTP_PORT=587
   SMTP_USERNAME=postmaster@statex.cz
   SMTP_PASSWORD=your-mailgun-smtp-password
   ```

### **SendGrid Setup**

1. **Sign up at SendGrid** (https://sendgrid.com)
2. **Verify your domain** `statex.cz`
3. **Get API credentials**:
   ```bash
   SENDGRID_API_KEY=your-sendgrid-api-key
   ```

4. **Configure notification service**:
   ```bash
   # In .env file
   SMTP_SERVER=smtp.sendgrid.net
   SMTP_PORT=587
   SMTP_USERNAME=apikey
   SMTP_PASSWORD=your-sendgrid-api-key
   ```

## 🔧 **Updated Notification Service**

The notification service will be updated to:
1. **Use professional email service** (Mailgun/SendGrid)
2. **Send from StateX email addresses** (contact@, admin@, sales@, etc.)
3. **Professional email templates** with StateX branding
4. **Reliable delivery** to user inboxes

## 📋 **Next Steps**

1. **Choose email service** (Mailgun recommended)
2. **Set up domain verification** for statex.cz
3. **Configure notification service** with new credentials
4. **Test email sending** with all StateX addresses
5. **Update email templates** with StateX branding

## 🎯 **Benefits of This Approach**

- ✅ **Professional**: Emails from your own domain
- ✅ **Reliable**: 99.9% deliverability
- ✅ **Scalable**: Handle thousands of emails
- ✅ **Maintenance-free**: No server management
- ✅ **Cost-effective**: Free tiers available
- ✅ **Easy setup**: 15-30 minutes

Would you like to proceed with Mailgun setup?
