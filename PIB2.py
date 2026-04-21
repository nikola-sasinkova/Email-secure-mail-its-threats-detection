import ssl
import mimetypes
import smtplib
from pathlib import Path
from email.message import EmailMessage
import getpass

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = "587"
SMTP_USER = "nika.sasinkova@gmail.com"
SMTP_PASSWORD = getpass.getpass("Zadaj heslo od Gmailu alebo App Password ")

if not SMTP_USER or not SMTP_PASSWORD:
    exit()

def create_email(subject, sender, recipients, body_text, attachment_paths: list):
    msg = EmailMessage()  # prazdny email
    msg["Subject"] = subject  
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    msg.set_content(body_text)

    if attachment_paths is not None:
        for p in attachment_paths:  
            
            if not p.is_file():
                raise FileNotFoundError(f"Priloha nebola najdena: {p}")  

            mime_type, _ = mimetypes.guess_type(p)  
            if mime_type is None:  
                mime_type = "application/octet-stream"  

            maintype, subtype = mime_type.split("/", 1)
            data = None
            with p.open("rb") as fp:
                data = fp.read()

            msg.add_attachment(
                data,
                maintype=maintype,
                subtype=subtype,
                filename=p.name,
            )

    return msg


def send_email(message):
    print("Posielam email")
    context = ssl.create_default_context()
    print("Pripajam sa do %s:%s", SMTP_HOST, SMTP_PORT)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(message)

    print(f"Sprava poslana: {message['To']}")


if __name__ == "__main__":
    SUBJECT = "Test"
    SENDER = "nika.sasinkova@gmail.com"
    RECIPIENTS = ["nikolka.sasinkova@gmail.com"]
    BODY_TEXT = """\
Test posielania emailu.
"""

    ATTACHMENTS = [
        Path("C:/Users/nikola/Pictures/Screenshots/test.png")
    ]

    msg = create_email(
        subject=SUBJECT,
        sender=SENDER,
        recipients=RECIPIENTS,
        body_text=BODY_TEXT,
        attachment_paths=ATTACHMENTS,
    )

    send_email(msg)

