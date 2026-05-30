from __future__ import annotations

import argparse
import mimetypes
import os
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from email.policy import default
from pathlib import Path
from typing import Any

from freelance_starter.paths import ensure_parent, project_path


@dataclass(frozen=True)
class SmtpConfig:
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = True
    timeout: int = 30


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def parse_recipients(value: str) -> list[str]:
    recipients = [
        item.strip()
        for chunk in value.split(";")
        for item in chunk.split(",")
        if item.strip()
    ]
    if not recipients:
        raise ValueError("At least one recipient email is required.")
    return recipients


def parse_bool(value: str | None, *, default_value: bool = True) -> bool:
    if value is None or value == "":
        return default_value
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def build_report_email(
    *,
    sender: str,
    recipients: list[str],
    subject: str,
    body: str,
    attachment_path: Path,
) -> EmailMessage:
    if not attachment_path.exists():
        raise FileNotFoundError(f"Attachment not found: {attachment_path}")
    if not sender:
        raise ValueError("Sender email is required.")
    if not recipients:
        raise ValueError("At least one recipient email is required.")

    message = EmailMessage()
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.set_content(body)

    content_type, _ = mimetypes.guess_type(attachment_path)
    if content_type is None:
        content_type = "application/octet-stream"
    maintype, subtype = content_type.split("/", 1)
    message.add_attachment(
        attachment_path.read_bytes(),
        maintype=maintype,
        subtype=subtype,
        filename=attachment_path.name,
    )
    return message


def save_email_preview(message: EmailMessage, output_path: Path) -> None:
    ensure_parent(output_path)
    output_path.write_bytes(message.as_bytes(policy=default))


def send_email(
    message: EmailMessage,
    config: SmtpConfig,
    *,
    smtp_factory: Any = smtplib.SMTP,
) -> None:
    with smtp_factory(config.host, config.port, timeout=config.timeout) as smtp:
        if config.use_tls:
            smtp.starttls()
        if config.username or config.password:
            smtp.login(config.username, config.password)
        smtp.send_message(message)


def smtp_config_from_env(*, timeout: int = 30) -> SmtpConfig:
    missing = [
        name
        for name in ("SMTP_HOST", "SMTP_USERNAME", "SMTP_PASSWORD")
        if not os.environ.get(name)
    ]
    if missing:
        missing_text = ", ".join(missing)
        raise ValueError(f"Missing SMTP environment variable(s): {missing_text}")

    return SmtpConfig(
        host=os.environ["SMTP_HOST"],
        port=int(os.environ.get("SMTP_PORT", "587")),
        username=os.environ["SMTP_USERNAME"],
        password=os.environ["SMTP_PASSWORD"],
        use_tls=parse_bool(os.environ.get("SMTP_USE_TLS"), default_value=True),
        timeout=timeout,
    )


def parse_args() -> argparse.Namespace:
    default_attachment = project_path(
        "projects", "03_api_report_tool", "output", "weather_report.xlsx"
    )
    default_preview = project_path(
        "projects", "04_email_report_sender", "output", "email_preview.eml"
    )
    default_env = project_path(
        "projects", "04_email_report_sender", "input", "email_settings.env"
    )

    parser = argparse.ArgumentParser(
        description="Build an email with a report attachment, then preview or send it."
    )
    parser.add_argument("--attachment", type=Path, default=default_attachment)
    parser.add_argument("--preview-output", type=Path, default=default_preview)
    parser.add_argument("--env-file", type=Path, default=default_env)
    parser.add_argument("--from-email", default=None)
    parser.add_argument("--to", default=None, help="Comma or semicolon separated recipients.")
    parser.add_argument("--subject", default="Daily automated report")
    parser.add_argument(
        "--body",
        default=(
            "Hi,\n\n"
            "Please find the latest automated report attached.\n\n"
            "Best,\nPython automation bot"
        ),
    )
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--send", action="store_true", help="Actually send via SMTP.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_env_file(args.env_file)

    sender = args.from_email or os.environ.get("EMAIL_FROM") or "reports@example.com"
    recipients_text = args.to or os.environ.get("EMAIL_TO") or "client@example.com"
    recipients = parse_recipients(recipients_text)

    message = build_report_email(
        sender=sender,
        recipients=recipients,
        subject=args.subject,
        body=args.body,
        attachment_path=args.attachment,
    )

    if args.send:
        config = smtp_config_from_env(timeout=args.timeout)
        send_email(message, config)
        print(f"Email sent to {len(recipients)} recipient(s) with {args.attachment.name}")
    else:
        save_email_preview(message, args.preview_output)
        print(f"Email preview saved: {args.preview_output}")
        print("Use --send with SMTP environment variables when you are ready to send.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
