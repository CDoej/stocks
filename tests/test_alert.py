import smtplib
from unittest.mock import patch, MagicMock
from src.alert import send_alert


class TestSendAlert:
    def _send(self, condition="below", trigger=270.0, actual=265.0):
        with patch("src.alert.smtplib.SMTP") as mock_smtp:
            instance = MagicMock()
            mock_smtp.return_value.__enter__.return_value = instance
            send_alert("Apple", "AAPL", "USD", condition, trigger, actual)
            return instance

    def test_sends_email(self):
        instance = self._send()
        instance.sendmail.assert_called_once()

    def test_subject_below(self):
        instance = self._send(condition="below", trigger=270.0, actual=265.0)
        _, _, raw = instance.sendmail.call_args[0]
        assert "fallen below" in raw
        assert "270.00" in raw

    def test_subject_above(self):
        instance = self._send(condition="above", trigger=220.0, actual=225.0)
        _, _, raw = instance.sendmail.call_args[0]
        assert "risen above" in raw
        assert "220.00" in raw

    def test_recipient(self):
        import src.config as config
        instance = self._send()
        _, recipient, _ = instance.sendmail.call_args[0]
        assert recipient == config.EMAIL_RECIPIENT
