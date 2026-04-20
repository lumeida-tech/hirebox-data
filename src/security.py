from dataclasses import dataclass
import os

from fastapi import HTTPException, Request, status

API_KEY_HEADER_NAME = "API_KEY"
FORWARDED_FOR_HEADER = "X-Forwarded-For"


def _parse_csv_env(var_name: str) -> frozenset[str]:
    raw_value = os.getenv(var_name, "")
    return frozenset(item.strip() for item in raw_value.split(",") if item.strip())


def _env_flag(var_name: str, default: str = "true") -> bool:
    value = os.getenv(var_name, default).strip().lower()
    return value in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class ApiSecuritySettings:
    enabled: bool
    api_key_prefix: str
    allowed_api_keys: frozenset[str]
    allowed_origins: frozenset[str]

    @classmethod
    def from_env(cls) -> "ApiSecuritySettings":
        return cls(
            enabled=_env_flag("HIREBOX_ENABLE_API_SECURITY", "true"),
            api_key_prefix=os.getenv("HIREBOX_API_KEY_PREFIX", "").strip(),
            allowed_api_keys=_parse_csv_env("HIREBOX_ALLOW_API_KEYS"),
            allowed_origins=_parse_csv_env("HIREBOX_ALLOW_ORIGINS"),
        )


def _extract_token(api_key_header: str, expected_prefix: str) -> str | None:
    candidate = api_key_header.strip()
    if not candidate:
        return None

    if not expected_prefix:
        return candidate

    if not candidate.startswith(expected_prefix):
        return None

    token = candidate.removeprefix(expected_prefix).strip()
    return token or None


def _get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get(FORWARDED_FOR_HEADER, "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    if request.client and request.client.host:
        return request.client.host

    return ""


async def verify_backend_request(request: Request) -> None:
    settings = ApiSecuritySettings.from_env()
    if not settings.enabled:
        return

    api_key_header = request.headers.get(API_KEY_HEADER_NAME)
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API_KEY header is required.",
        )

    token = _extract_token(api_key_header, settings.api_key_prefix)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: invalid API_KEY format.",
        )

    if token not in settings.allowed_api_keys:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: API key is not allowed.",
        )

    client_ip = _get_client_ip(request)
    if client_ip not in settings.allowed_origins:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: IP address is not allowed.",
        )

    request.state.client_ip = client_ip
    request.state.api_key_token = token
