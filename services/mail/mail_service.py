class Mail:

    @staticmethod
    def send_email(recipient_email: str, subject: str, body: str):
        from settings.settings import settings
        from email.message import EmailMessage
        import smtplib

        gmail_user = settings.MAIL_USERNAME
        gmail_password = settings.MAIL_PASSWORD
        message = EmailMessage()
        body = body
        message.set_content(body)
        message['Subject'] = subject
        message['From'] = gmail_user
        message['To'] = recipient_email
        server = smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(message)
        server.close()