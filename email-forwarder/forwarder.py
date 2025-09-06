#!/usr/bin/env python3
"""
StateX Email Forwarder

Forwards all emails from StateX addresses to your personal Gmail.
"""

import os
import time
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.message import MIMEMessage
import logging

# Configuration
FORWARD_TO = os.getenv("FORWARD_TO", "ssfskype@gmail.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "email-server")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
MAIL_DIR = "/var/mail"

# StateX email addresses
STATEX_EMAILS = [
    "contact@statex.cz",
    "admin@statex.cz", 
    "sales@statex.cz",
    "sergej@statex.cz",
    "support@statex.cz"
]

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def forward_email(original_email_path):
    """Forward a single email to Gmail"""
    try:
        # Read the original email
        with open(original_email_path, 'r', encoding='utf-8', errors='ignore') as f:
            original_content = f.read()
        
        # Parse the email
        msg = email.message_from_string(original_content)
        
        # Extract headers
        from_addr = msg.get('From', 'Unknown')
        to_addr = msg.get('To', 'Unknown')
        subject = msg.get('Subject', 'No Subject')
        date = msg.get('Date', 'Unknown')
        
        logger.info(f"Forwarding email from {from_addr} to {to_addr}: {subject}")
        
        # Create forwarded message
        forward_msg = MIMEMultipart()
        forward_msg['From'] = to_addr  # Original recipient becomes sender
        forward_msg['To'] = FORWARD_TO
        forward_msg['Subject'] = f"[FORWARDED] {subject}"
        forward_msg['Reply-To'] = to_addr  # So you can reply to original sender
        
        # Create forwarded body
        body = f"""
This email was forwarded from your StateX email system.

Original From: {from_addr}
Original To: {to_addr}
Original Date: {date}
Original Subject: {subject}

--- Original Message ---
"""
        
        # Add original message
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload()
                    break
        else:
            body += msg.get_payload()
        
        forward_msg.attach(MIMEText(body, 'plain'))
        
        # Send via Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('ssfskype@gmail.com', 'your-app-password')  # You'll need to set this
        server.send_message(forward_msg)
        server.quit()
        
        logger.info(f"Successfully forwarded email: {subject}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to forward email: {e}")
        return False

def monitor_mailbox():
    """Monitor mailbox for new emails"""
    logger.info("Starting email forwarder...")
    logger.info(f"Forwarding emails to: {FORWARD_TO}")
    logger.info(f"Monitoring StateX emails: {', '.join(STATEX_EMAILS)}")
    
    while True:
        try:
            # Check for new emails in mail directory
            if os.path.exists(MAIL_DIR):
                for filename in os.listdir(MAIL_DIR):
                    if filename.startswith('statex'):
                        email_path = os.path.join(MAIL_DIR, filename)
                        if os.path.isfile(email_path):
                            forward_email(email_path)
                            # Move processed email
                            processed_path = email_path + '.processed'
                            os.rename(email_path, processed_path)
            
            time.sleep(10)  # Check every 10 seconds
            
        except Exception as e:
            logger.error(f"Error in monitor loop: {e}")
            time.sleep(30)

if __name__ == "__main__":
    monitor_mailbox()
