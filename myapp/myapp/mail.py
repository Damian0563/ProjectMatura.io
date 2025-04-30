import os
from dotenv import load_dotenv
import smtplib
load_dotenv()

def account_creation(mail):
    subject = "Potwierdzenie utworzenia konta na ProjectMatura.io"
    message = f"""\
    Dzień Dobry,

        Dziękujemy za utworzenie konta na platformie ProjectMatura.io. Ten mail jest potwierdzeniem utworzenia konta.Jeżeli Pan/Pani nie utworzył konta w naszym serwisie, prosimy o niezwłoczny kontakt.

    Z poważaniem,
    ProjectMatura.io
    """
    text = f"Subject: {subject}\nTo: {mail}\nFrom: projectmatura.io@gmail.com\n\n{message}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login('projectmatura.io@gmail.com', os.getenv('GMAIL_PASS'))
    server.sendmail('projectmatura.io@gmail.com', mail, text.encode('utf-8'))
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