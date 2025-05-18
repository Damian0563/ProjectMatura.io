import os
from . import postgresql
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
load_dotenv()

def account_creation(mail):

    code=postgresql.generate_auth(mail)
    html = f"""\
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;font-size:20px;">
        <h2>Witamy na platformie ProjectMatura.io!</h2>
        <p>Dzień Dobry,</p>
        <p>
        Dziękujemy za utworzenie konta na platformie <strong>ProjectMatura.io</strong>.
        Ten mail jest potwierdzeniem utworzenia konta.<br>Oto Pani/Pana kod autoryzacji: <strong style="font-size:28px">{code}</strong>
        </p>
        <p>Z poważaniem,<br><em>ProjectMatura.io</em></p>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Potwierdzenie utworzenia konta na ProjectMatura.io"
    msg["From"] = "projectmatura.io@gmail.com"
    msg["To"] = mail
    # Optional plain text version
    plain_message = """\
    Dzień Dobry,

    Dziękujemy za utworzenie konta na platformie ProjectMatura.io. 
    Ten mail jest potwierdzeniem utworzenia konta. 
    Jeżeli Pan/Pani nie utworzył konta w naszym serwisie, prosimy o niezwłoczny kontakt.

    Z poważaniem,
    ProjectMatura.io
    """

    # Attach both plain and HTML versions (email clients fall back to plain if needed)
    msg.attach(MIMEText(plain_message, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login('projectmatura.io@gmail.com', os.getenv('GMAIL_PASS'))
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()

def payment(mail):
    subject = "Potwierdzenie zakupu subskrypcji na ProjectMatura.io"
    message = f"""\
    Dzień Dobry,

        Dziękujemy za zakup subskrypcji na platformie ProjectMatura.io. Ten mail jest potwierdzeniem zakupu. Jeżeli Pan/Pani nie dokonał zakupu w naszym serwisie, prosimy o niezwłoczny kontakt.

    Z poważaniem,
    ProjectMatura.io
    """
    text = f"Subject: {subject}\nTo: {mail}\nFrom: projectmatura.io@gmail.com\n\n{message}"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login('projectmatura.io@gmail.com', os.getenv('GMAIL_PASS'))
    server.sendmail('projectmatura.io@gmail.com', mail, text.encode('utf-8'))
    server.quit()

def cancelation(mail):
    subject = "Anulacja subskrypcji na ProjectMatura.io"
    message = f"""\
    Dzień Dobry,

        Informujemy o anulowaniu subskrypcji na platformie ProjectMatura.io.

    Z poważaniem,
    ProjectMatura.io
    """
    text = f"Subject: {subject}\nTo: {mail}\nFrom: projectmatura.io@gmail.com\n\n{message}"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login('projectmatura.io@gmail.com', os.getenv('GMAIL_PASS'))
    server.sendmail('projectmatura.io@gmail.com', mail, text.encode('utf-8'))
    server.quit()