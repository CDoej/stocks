import smtplib
from email.mime.text import MIMEText
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT, SMTP_HOST, SMTP_PORT


def send_alert(name: str, symbol: str, currency: str, condition: str, trigger_price: float, actual_price: float):
    direction = "risen above" if condition == "above" else "fallen below"
    subject = f"Stock Alert: {name} has {direction} {currency} {trigger_price:.2f}"
    body = (
        f"{name} ({symbol}) is currently trading at {currency} {actual_price:.2f}, "
        f"which has {direction} your target of {currency} {trigger_price:.2f}."
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())

    print(f"Alert sent: {subject}")
