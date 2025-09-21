import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP server configuration
SMTP_SERVER = "smtp.office365.com"    # e.g. smtp.gmail.com
SMTP_PORT = 587                     # 587 for TLS, 465 for SSL
USERNAME = "fawtara@becom.ly"
PASSWORD = "G8zMtn3yXjj"

# Email details
FROM_EMAIL = USERNAME
TO_EMAIL = "m.fathalla@wassel.ly"
SUBJECT = "SMTP Test Email"
BODY = "Hello! This is a test email from Python."

try:
    # Create email message
    msg = MIMEMultipart()
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = SUBJECT
    msg.attach(MIMEText(BODY, "plain"))

    # Connect to the SMTP server
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Secure the connection
    server.login(USERNAME, PASSWORD)
    server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
    server.quit()

    print("✅ Email sent successfully!")

except Exception as e:
    print(f"❌ Failed to send email: {e}")
