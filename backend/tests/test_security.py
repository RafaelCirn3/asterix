from datetime import timedelta

from app.core.security import create_access_token, decode_access_token_payload, get_password_hash, verify_password


def test_password_hash_roundtrip() -> None:
    hashed = get_password_hash("SenhaSegura123!")
    assert hashed != "SenhaSegura123!"
    assert verify_password("SenhaSegura123!", hashed)
    assert not verify_password("senha-incorreta", hashed)


def test_access_token_contains_jti_and_subject() -> None:
    token = create_access_token(123, expires_delta=timedelta(minutes=5))
    payload = decode_access_token_payload(token)
    assert payload is not None
    assert payload["sub"] == "123"
    assert payload.get("jti")
    assert payload.get("iat")
    assert payload.get("exp")
