#!/usr/bin/env python3

from email import policy
from email.parser import BytesParser
from typing import Any
import argparse
import json

TARGET_HEADERS = [
    "From", "To", "Delivered-To", "Deliver-To", "Subject",
    "Reply-To", "Return-Path", "Received", "Message-ID",
    "DKIM-Signature", "Authentication-Results"
]

def parse_email_headers(file_path) -> dict[Any, Any]:
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    extracted = {}

    for header in TARGET_HEADERS:
        if header == "Received":
            extracted[header] = msg.get_all("Received") or []
        else:
            extracted[header] = msg.get(header) or None

    spf_result = None
    auth_results = extracted.get("Authentication-Results")
    if auth_results and "spf=" in auth_results.lower():
        for part in auth_results.split(";"):
            part = part.strip()
            if part.lower().startswith("spf="):
                spf_result = part
                break

    extracted["SPF"] = spf_result
    extracted["DKIM"] = extracted.pop("DKIM-Signature")

    return extracted

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze email headers from a .eml file."
    )

    parser.add_argument(
        "file_path",
        help="Path to the .eml file"
    )

    args = parser.parse_args()

    result = parse_email_headers(args.file_path)
    print(json.dumps(result, indent=4, default=str))

if __name__ == "__main__":
    main()