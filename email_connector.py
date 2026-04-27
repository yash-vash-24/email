"""
Simple Email Connector - Works with any email provider
Supports: Gmail, Outlook, Yahoo, and standard IMAP/SMTP
"""

import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email
from datetime import datetime

# Email provider configurations
EMAIL_CONFIG = {
    'gmail': {
        'imap_host': 'imap.gmail.com',
        'smtp_host': 'smtp.gmail.com',
        'imap_port': 993,
        'smtp_port': 587
    },
    'outlook': {
        'imap_host': 'outlook.office365.com',
        'smtp_host': 'outlook.office365.com',
        'imap_port': 993,
        'smtp_port': 587
    },
    'yahoo': {
        'imap_host': 'imap.mail.yahoo.com',
        'smtp_host': 'smtp.mail.yahoo.com',
        'imap_port': 993,
        'smtp_port': 587
    }
}


class SimpleEmailConnector:
    """Connect to any email provider with just email & password"""
    
    def __init__(self, email, password, provider='gmail'):
        """
        Initialize email connection
        
        Args:
            email: Your email address
            password: Your password (or app-specific password)
            provider: 'gmail', 'outlook', 'yahoo', or 'custom'
        """
        self.email = email
        self.password = password
        self.provider = provider.lower()
        
        if self.provider in EMAIL_CONFIG:
            config = EMAIL_CONFIG[self.provider]
            self.imap_host = config['imap_host']
            self.smtp_host = config['smtp_host']
            self.imap_port = config['imap_port']
            self.smtp_port = config['smtp_port']
        else:
            # For custom providers, ask user
            self.imap_host = None
            self.smtp_host = None
        
        self.imap = None
        self.connect_imap()
    
    def connect_imap(self):
        """Connect to email via IMAP"""
        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
            self.imap.login(self.email, self.password)
            print(f"✅ Connected to {self.provider}!")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def get_emails(self, max_count=10):
        """
        Fetch recent emails
        
        Args:
            max_count: Number of emails to fetch
            
        Returns:
            List of email dictionaries
        """
        try:
            self.imap.select('INBOX')
            
            # Get email IDs
            status, email_ids = self.imap.search(None, 'ALL')
            email_list = email_ids[0].split()[-max_count:]  # Get last N emails
            
            emails = []
            for e_id in reversed(email_list):
                status, msg_data = self.imap.fetch(e_id, '(RFC822)')
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        emails.append({
                            'id': e_id.decode(),
                            'from': msg.get('From', 'Unknown'),
                            'to': msg.get('To', ''),
                            'subject': msg.get('Subject', 'No Subject'),
                            'body': self._get_body(msg),
                            'date': msg.get('Date', '')
                        })
            
            return emails
        except Exception as e:
            print(f"❌ Error fetching emails: {e}")
            return []
    
    def _get_body(self, msg):
        """Extract email body"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode('utf-8')
                        break
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8')
            except:
                body = msg.get_payload()
        
        return body if body else "(No text body)"
    
    def send_reply(self, to_address, subject, body):
        """
        Send an email
        
        Args:
            to_address: Recipient email
            subject: Email subject
            body: Email body
        """
        try:
            # Create message
            msg = MIMEText(body)
            msg['From'] = self.email
            msg['To'] = to_address
            msg['Subject'] = subject
            
            # Connect SMTP
            smtp = smtplib.SMTP(self.smtp_host, self.smtp_port)
            smtp.starttls()
            smtp.login(self.email, self.password)
            
            # Send
            smtp.send_message(msg)
            smtp.quit()
            
            print(f"✅ Email sent to {to_address}")
            return True
        
        except Exception as e:
            print(f"❌ Failed to send: {e}")
            return False
    
    def disconnect(self):
        """Close connection"""
        if self.imap:
            self.imap.close()
            self.imap.logout()
            print("✅ Disconnected")


# Test
if __name__ == '__main__':
    # Example
    # connector = SimpleEmailConnector('your_email@gmail.com', 'your_password', 'gmail')
    # emails = connector.get_emails(5)
    # for email in emails:
    #     print(f"From: {email['from']}, Subject: {email['subject']}")
    pass
