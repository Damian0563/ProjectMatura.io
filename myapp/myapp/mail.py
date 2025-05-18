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
    html="""\
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;font-size:20px;">
    <h2> Dziękujemy za zakup subskrypcji na platformie ProjectMatura.io!</h2>
        <p>Dzień Dobry,</p>
        <p>
        Ten mail jest potwierdzeniem zakupu subskrypcji. Teraz ma Pan/Pani dostęp do następujących treści na platformie:<br>
        <li>Liczby Rzeczywiste</li>
        <li>Logarytmy</li>
        <li>Równania i nierówności</li>
        <li>Trygonometria</li>
        <li>Geometria</li>
        <li>Planimetria</li>
        <li>Kombinatoryka</li>
        <li>Prawdopodobieństwo</li>
        <li>Okręgi</li>
        <li>Ciągi</li>
        <li>Zadania Optymalizacyjne</li>
        <li>Podsumowanie</li>
        Jeżeli Pan/Pani nie dokonał zakupu w naszym serwisie, prosimy o niezwłoczny kontakt.
        </p>
        <p>Z poważaniem,<br><em>ProjectMatura.io</em></p>
    </body>
    </html>
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Potwierdzenie zakupu subskrypcji na ProjectMatura.io"
    msg["From"] = "projectmatura.io@gmail.com"
    msg["To"] = mail
    # Optional plain text version
    plain_message = """\
    Dzień Dobry,

    Dziękujemy za zakup subskrypcji na platformie ProjectMatura.io. 
    Ten mail jest potwierdzeniem zakupu subskrypcji. Teraz ma Pan/Pani dostęp do następujących treści na platformie:
        Liczby Rzeczywiste
        Logarytmy
        Równania i nierówności
        Trygonometria
        Geometria
        Planimetria
        Kombinatoryka
        Prawdopodobieństwo
        Okręgi
        Ciągi
        Zadania Optymalizacyjne
        Podsumowanie
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

def cancelation(mail):
    html = f"""\
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;font-size:20px;">
        <p>Dzień Dobry,</p>
        <p>
        Informujemy o rezygnacji z subskrypcji na platformie <strong>ProjectMatura.io</strong>.
        Utraci Pan/Pani dostęp do wszystkich płatnych rozdziałow.
        </p>
        <p>Z poważaniem,<br><em>ProjectMatura.io</em></p>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Potwierdzenie rezygnacji z subskrypcji na ProjectMatura.io"
    msg["From"] = "projectmatura.io@gmail.com"
    msg["To"] = mail
    plain_message = """\
    Dzień Dobry,

    Informujemy o rezygnacji z subskrypcji na platformie <strong>ProjectMatura.io</strong>.
    Utraci Pan/Pani dostęp do wszystkich płatnych rozdziałow.

    Z poważaniem,
    ProjectMatura.io
    """

    msg.attach(MIMEText(plain_message, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login('projectmatura.io@gmail.com', os.getenv('GMAIL_PASS'))
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()