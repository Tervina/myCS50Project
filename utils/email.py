import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
import os

def send_password_reset_email(recipient_email, reset_link):
    """Send password reset email"""
    sender_email = "your-email@example.com"  # Replace with your email
    password = Config.EMAIL_PASSWORD
    
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Password Reset Request"
    
    # Email body
    body = f"""
    Hello,
    
    You requested a password reset. Please click the link below to reset your password:
    
    {reset_link}
    
    If you did not request this, please ignore this email.
    
    Thank you,
    Your Website Team
    """
    
    message.attach(MIMEText(body, "plain"))
    
    # Send email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def send_order_confirmation_email(recipient_email, order_summary):
    """Send order confirmation email"""
    try:
        sender_email = "tervina.samir012@gmail.com"  # Replace with your email
        password = Config.EMAIL_PASSWORD
        
        if not password:
            raise ValueError("EMAIL_PASSWORD is missing!")
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Order Confirmation"
        message["From"] = sender_email
        message["To"] = recipient_email
        
        part = MIMEText(order_summary, "plain")
        message.attach(part)
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False