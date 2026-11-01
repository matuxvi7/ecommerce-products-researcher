from urllib.parse import urlsplit


ALLOWED_FIELDS = {
    "name",
    "category",
    "description",
    "sku",
    "url",
}


def validate_product_payload(payload):
    if not isinstance(payload, dict):
        return None, ["El cuerpo debe ser un objeto JSON"]

    errors = []
    unknown_fields = set(payload) - ALLOWED_FIELDS

    if unknown_fields:
        errors.append(
            f"Campos no permitidos: {', '.join(sorted(unknown_fields))}"
        )

    name = payload.get("name")

    if not isinstance(name, str) or not name.strip():
        errors.append("El campo 'name' es obligatorio y debe ser texto")
    elif len(name.strip()) > 255:
        errors.append("'name' no puede superar los 255 caracteres")

    limits = {
        "category": 100,
        "description": None,
        "sku": 100,
        "url": 2048,
    }

    for field, max_length in limits.items():
        value = payload.get(field)

        if value is None or value == "":
            continue

        if not isinstance(value, str):
            errors.append(f"'{field}' debe ser texto")
            continue

        if max_length and len(value.strip()) > max_length:
            errors.append(
                f"'{field}' no puede superar los {max_length} caracteres"
            )

    url = payload.get("url")

    if isinstance(url, str) and url.strip():
        parsed = urlsplit(url.strip())

        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            errors.append("'url' debe ser una URL HTTP o HTTPS válida")

    if errors:
        return None, errors

    data = {
        "name": name.strip(),
        "category": payload.get("category") or None,
        "description": payload.get("description") or None,
        "sku": payload.get("sku") or None,
        "url": payload.get("url") or None,
    }

    return data, []