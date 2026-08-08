#!/usr/bin/env python3
"""Translate English text with Tencent TMT using credentials in macOS Keychain."""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import hashlib
import hmac
import json
import subprocess
import sys
import time


HOST = "tmt.tencentcloudapi.com"
SERVICE = "tmt"
ACTION = "TextTranslate"
VERSION = "2018-03-21"
REGION = "ap-guangzhou"
TERM_REPO_ID = "b21065518ea611f18bb32f3360e0816a"
NETWORK_INTERFACE = "en0"


def keychain_password(service: str) -> str:
    result = subprocess.run(
        [
            "security",
            "find-generic-password",
            "-a",
            "codex-tmt",
            "-s",
            service,
            "-w",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def sign(key: bytes, message: str) -> bytes:
    return hmac.new(key, message.encode("utf-8"), hashlib.sha256).digest()


@functools.lru_cache(maxsize=4)
def resolve_real_ips(host: str) -> list[str]:
    """Resolve outside Clash fake-IP DNS without changing its global mode."""
    query = subprocess.run(
        [
            "curl",
            "--silent",
            "--show-error",
            "--max-time",
            "15",
            "--header",
            "accept: application/dns-json",
            f"https://1.1.1.1/dns-query?name={host}&type=A",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(query.stdout)
    return [
        answer["data"]
        for answer in data.get("Answer", [])
        if answer.get("type") == 1
    ]


def post_direct(headers: dict[str, str], payload: str) -> dict:
    """POST through the active network path, with direct-IP fallback.

    The normal request must come first.  On Macs using a global proxy, forcing
    the physical interface and an external DNS-over-HTTPS lookup can make the
    API unreachable even though the signed Tencent endpoint itself works.
    """
    failures: list[str] = []
    command = [
        "curl",
        "--silent",
        "--show-error",
        "--max-time",
        "30",
        "--request",
        "POST",
    ]
    for name, value in headers.items():
        command.extend(["--header", f"{name}: {value}"])
    command.extend(["--data-binary", "@-", f"https://{HOST}"])
    response = subprocess.run(
        command,
        input=payload,
        capture_output=True,
        text=True,
    )
    if response.returncode == 0:
        try:
            return json.loads(response.stdout)
        except json.JSONDecodeError:
            failures.append("normal route returned invalid JSON")
    else:
        failures.append(response.stderr.strip())

    for address in resolve_real_ips(HOST):
        command = [
            "curl",
            "--interface",
            NETWORK_INTERFACE,
            "--silent",
            "--show-error",
            "--max-time",
            "30",
            "--request",
            "POST",
            "--resolve",
            f"{HOST}:443:{address}",
        ]
        for name, value in headers.items():
            command.extend(["--header", f"{name}: {value}"])
        command.extend(["--data-binary", "@-", f"https://{HOST}"])
        response = subprocess.run(
            command,
            input=payload,
            capture_output=True,
            text=True,
        )
        if response.returncode == 0:
            return json.loads(response.stdout)
        failures.append(response.stderr.strip())
    raise RuntimeError("Tencent TMT connection failed: " + "; ".join(failures))


def translate(source_text: str, *, use_glossary: bool = True) -> dict:
    secret_id = keychain_password("Tencent TMT SecretId")
    secret_key = keychain_password("Tencent TMT SecretKey")

    request_body = {
        "SourceText": source_text,
        "Source": "en",
        "Target": "zh",
        "ProjectId": 0,
    }
    if use_glossary:
        request_body["TermRepoIDList"] = [TERM_REPO_ID]
    payload = json.dumps(
        request_body,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    timestamp = int(time.time())
    date = dt.datetime.fromtimestamp(timestamp, dt.UTC).strftime("%Y-%m-%d")

    canonical_headers = (
        "content-type:application/json; charset=utf-8\n"
        f"host:{HOST}\n"
        f"x-tc-action:{ACTION.lower()}\n"
    )
    signed_headers = "content-type;host;x-tc-action"
    hashed_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = "\n".join(
        ["POST", "/", "", canonical_headers, signed_headers, hashed_payload]
    )

    algorithm = "TC3-HMAC-SHA256"
    credential_scope = f"{date}/{SERVICE}/tc3_request"
    string_to_sign = "\n".join(
        [
            algorithm,
            str(timestamp),
            credential_scope,
            hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
        ]
    )
    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, SERVICE)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(
        secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    authorization = (
        f"{algorithm} Credential={secret_id}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )

    return post_direct(
        {
            "Authorization": authorization,
            "Content-Type": "application/json; charset=utf-8",
            "Host": HOST,
            "X-TC-Action": ACTION,
            "X-TC-Timestamp": str(timestamp),
            "X-TC-Version": VERSION,
            "X-TC-Region": REGION,
        },
        payload,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", help="English text to translate")
    parser.add_argument(
        "--no-glossary", action="store_true", help="disable the Tencent term repository"
    )
    args = parser.parse_args()
    if len(args.text) > 1900:
        parser.error("text must be 1,900 characters or fewer")

    result = translate(args.text, use_glossary=not args.no_glossary)
    response = result.get("Response", {})
    if "Error" in response:
        error = response["Error"]
        print(f"{error.get('Code')}: {error.get('Message')}", file=sys.stderr)
        return 1
    print(response.get("TargetText", ""))
    if "UsedAmount" in response:
        print(f"used characters: {response['UsedAmount']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
