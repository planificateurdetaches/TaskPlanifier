import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_reset_password_email(email, reset_link):
    sender_email = "TaskPlanifier@gmail.com"
    sender_password = "zuba qugq ndrr qpei"
    smtp_server = "smtp.gmail.com"
    smtp_port = 465

    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset Request"
    message["From"] = sender_email
    message["To"] = email

    text = f"""\
    Hi,
    Click the link below to reset your password:
    {reset_link}
    """
    html = f"""\
    <html>
    <body>
        <p>Hi,<br>
        Click the link below to reset your password:<br>
        <a href="{reset_link}">Reset Password</a>
        </p>
    </body>
    </html>
    """
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            print("SMTP connection and login successful.")  # Debugging information
            server.sendmail(sender_email, email, message.as_string())
            print(f"Email sent successfully to {email}.")  # Debugging information
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_email = "ettoumiyves@gmail.com"
    test_link = "http://localhost:8501/reset_password"
    send_reset_password_email(test_email, test_link)


