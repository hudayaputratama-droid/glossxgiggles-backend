import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
from models import Booking
from datetime import datetime

class EmailService:
    def __init__(self):
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.sender_email = settings.smtp_user
        self.sender_password = settings.smtp_password
    
    def send_email(self, recipient: str, subject: str, html_content: str):
        """Send email"""
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient
            
            part = MIMEText(html_content, "html")
            message.attach(part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient, message.as_string())
            
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def send_booking_confirmation(self, customer_email: str, booking_code: str, booking_date: str, total_price: float):
        """Send booking confirmation email"""
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Booking Confirmation - GLOSS x GIGGLES</h2>
                <p>Thank you for booking with us!</p>
                <div style="background-color: #f0f0f0; padding: 20px; border-radius: 5px;">
                    <p><strong>Booking Code:</strong> {booking_code}</p>
                    <p><strong>Date:</strong> {booking_date}</p>
                    <p><strong>Total Price:</strong> ${total_price:.2f}</p>
                </div>
                <p>Please arrive 10 minutes before your appointment.</p>
                <p>Questions? Contact us at hello@glossxgiggles.com</p>
            </body>
        </html>
        """
        return self.send_email(customer_email, "Booking Confirmation", html_content)
    
    def send_appointment_reminder(self, customer_email: str, booking_date: str, booking_time: str):
        """Send appointment reminder email"""
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Appointment Reminder - GLOSS x GIGGLES</h2>
                <p>Your appointment is coming up!</p>
                <div style="background-color: #FFB6C1; padding: 20px; border-radius: 5px;">
                    <p><strong>Date:</strong> {booking_date}</p>
                    <p><strong>Time:</strong> {booking_time}</p>
                </div>
                <p>We look forward to seeing you!</p>
            </body>
        </html>
        """
        return self.send_email(customer_email, "Appointment Reminder", html_content)
