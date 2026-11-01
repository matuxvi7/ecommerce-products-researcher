import re
import unicodedata
from urllib.parse import (
    urlsplit,
    urlunsplit,
    parse_qsl,
    urlencode,
)


def normalize_text(value: str | None) -> str:
    if not value:
        return ""

    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(
        char for char in value
        if not unicodedata.combining(char)
    )

    value = re.sub(r"[^a-z0-9]+", " ", value)

    return " ".join(value.split())


def normalize_product_name(name: str) -> str:
    return normalize_text(name)


def normalize_category(
    category: str | None,
    aliases: dict[str, str] | None = None,
) -> str | None:
    if not category:
        return None

    normalized = normalize_text(category)

    if aliases:
        normalized_aliases = {
            normalize_text(alias): canonical
            for alias, canonical in aliases.items()
        }

        return normalized_aliases.get(normalized, normalized)

    return normalized


def normalize_sku(sku: str | None) -> str | None:
    if not sku:
        return None

    normalized = sku.strip().upper()

    return normalized or None


def normalize_url(url: str | None) -> str | None:
    if not url:
        return None

    parts = urlsplit(url.strip())

    if not parts.hostname:
        return None

    hostname = parts.hostname.lower().removeprefix("www.")

    if parts.port:
        hostname = f"{hostname}:{parts.port}"

    path = parts.path.rstrip("/") or "/"

    tracking_parameters = {
        "fbclid",
        "gclid",
    }

    query_parameters = [
        (key, value)
        for key, value in parse_qsl(
            parts.query,
            keep_blank_values=True,
        )
        if not key.lower().startswith("utm_")
        and key.lower() not in tracking_parameters
    ]

    query_parameters.sort()

    return urlunsplit((
        "https",
        hostname,
        path,
        urlencode(query_parameters),
        "",
    ))