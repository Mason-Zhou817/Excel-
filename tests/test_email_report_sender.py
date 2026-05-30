from __future__ import annotations

from email.message import EmailMessage
from pathlib import Path

import pytest

from freelance_starter.email_report_sender import (
    SmtpConfig,
    build_report_email,
    parse_recipients,
    save_email_preview,
    send_email,
)


class FakeSmtp:
    instances: list["FakeSmtp"] = []

    def __init__(self, host: str, port: int, timeout: int) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.started_tls = False
        self.login_args: tuple[str, str] | None = None
        self.sent_message: EmailMessage | None = None
        FakeSmtp.instances.append(self)

    def __enter__(self) -> "FakeSmtp":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def starttls(self) -> None:
        self.started_tls = True

    def login(self, username: str, password: str) -> None:
        self.login_args = (username, password)

    def send_message(self, message: EmailMessage) -> None:
        self.sent_message = message


def test_parse_recipients_accepts_commas_and_semicolons() -> None:
    assert parse_recipients("a@example.com,b@example.com; c@example.com") == [
        "a@example.com",
        "b@example.com",
        "c@example.com",
    ]


def test_parse_recipients_rejects_empty_input() -> None:
    with pytest.raises(ValueError, match="recipient"):
        parse_recipients(" , ; ")


def test_build_report_email_attaches_file(tmp_path: Path) -> None:
    attachment = tmp_path / "report.xlsx"
    attachment.write_bytes(b"example report")

    message = build_report_email(
        sender="reports@example.com",
        recipients=["client@example.com"],
        subject="Weekly report",
        body="Attached.",
        attachment_path=attachment,
    )

    assert message["From"] == "reports@example.com"
    assert message["To"] == "client@example.com"
    assert message["Subject"] == "Weekly report"
    attachments = list(message.iter_attachments())
    assert len(attachments) == 1
    assert attachments[0].get_filename() == "report.xlsx"


def test_save_email_preview_writes_eml_file(tmp_path: Path) -> None:
    attachment = tmp_path / "report.xlsx"
    attachment.write_bytes(b"example report")
    output = tmp_path / "email_preview.eml"
    message = build_report_email(
        sender="reports@example.com",
        recipients=["client@example.com"],
        subject="Report preview",
        body="Attached.",
        attachment_path=attachment,
    )

    save_email_preview(message, output)

    content = output.read_text(encoding="utf-8")
    assert "Subject: Report preview" in content
    assert "report.xlsx" in content


def test_send_email_uses_smtp_config(tmp_path: Path) -> None:
    FakeSmtp.instances.clear()
    attachment = tmp_path / "report.xlsx"
    attachment.write_bytes(b"example report")
    message = build_report_email(
        sender="reports@example.com",
        recipients=["client@example.com"],
        subject="Send report",
        body="Attached.",
        attachment_path=attachment,
    )

    send_email(
        message,
        SmtpConfig(
            host="smtp.example.com",
            port=587,
            username="reports@example.com",
            password="secret",
            timeout=10,
        ),
        smtp_factory=FakeSmtp,
    )

    smtp = FakeSmtp.instances[0]
    assert smtp.host == "smtp.example.com"
    assert smtp.port == 587
    assert smtp.timeout == 10
    assert smtp.started_tls is True
    assert smtp.login_args == ("reports@example.com", "secret")
    assert smtp.sent_message is message
