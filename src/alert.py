import logging
import smtplib
from email.mime.text import MIMEText
from src.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT, SMTP_HOST, SMTP_PORT

logger = logging.getLogger(__name__)


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

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        logger.info(f"Alert sent: {subject}")
    except Exception as exc:
        # Log and continue — a failed alert shouldn't abort the rest of the run.
        logger.error(f"Failed to send alert '{subject}': {exc}")
