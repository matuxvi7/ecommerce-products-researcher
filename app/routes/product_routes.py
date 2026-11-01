import csv
import io

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from app.db import db
from app.schemas.product_schema import validate_product_payload
from app.services.discovery_service import DiscoveryService


product_bp = Blueprint("products", __name__, url_prefix="/api/products")


def serialize_product(product):
    return {
        "id": product.id,
        "name": product.name,
        "normalized_name": product.normalized_name,
        "category": product.category,
        "description": product.description,
        "sku": product.sku,
        "url": product.canonical_url,
        "status": product.status,
    }


@product_bp.route("", methods=["POST"])
def create_product():
    payload = request.get_json(silent=True)

    data, errors = validate_product_payload(payload)

    if errors:
        return jsonify({
            "error": "validation_error",
            "details": errors,
        }), 400

    try:
        service = DiscoveryService(db.session)
        result = service.discover_product(**data)

        db.session.commit()

        return jsonify({
            "created": result.created,
            "duplicate_reason": result.duplicate_reason,
            "similarity": result.similarity,
            "product": serialize_product(result.product),
        }), 201 if result.created else 200

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "error": "integrity_error",
            "message": "El SKU o la URL ya están asociados a otro producto.",
        }), 409

    except Exception:
        db.session.rollback()
        raise


@product_bp.route("/import-csv", methods=["POST"])
def import_products_csv():
    file = request.files.get("file")

    if file is None or not file.filename:
        return jsonify({
            "error": "validation_error",
            "message": "Debés adjuntar un archivo CSV en el campo 'file'.",
        }), 400

    try:
        content = file.read().decode("utf-8-sig")
    except UnicodeDecodeError:
        return jsonify({
            "error": "invalid_encoding",
            "message": "El archivo debe utilizar codificación UTF-8.",
        }), 400

    try:
        reader = csv.DictReader(io.StringIO(content))

        if not reader.fieldnames:
            return jsonify({
                "error": "invalid_csv",
                "message": "El CSV está vacío o no contiene encabezados.",
            }), 400

        headers = reader.fieldnames

        if len(headers) != len(set(headers)):
            return jsonify({
                "error": "invalid_csv",
                "message": "El CSV contiene encabezados duplicados.",
            }), 400

        if "name" not in headers:
            return jsonify({
                "error": "invalid_csv",
                "message": "El CSV debe contener la columna obligatoria 'name'.",
            }), 400

        unknown_headers = set(headers) - {
            "name", "category", "description", "sku", "url"
        }

        if unknown_headers:
            return jsonify({
                "error": "invalid_csv",
                "message": f"Columnas no permitidas: {', '.join(sorted(unknown_headers))}",
            }), 400

        validated_rows = []
        row_errors = []

        for row_number, row in enumerate(reader, start=2):
            if None in row:
                row_errors.append({
                    "row": row_number,
                    "errors": ["La fila contiene más columnas que el encabezado."],
                })
                continue

            if not any(value and value.strip() for value in row.values()):
                continue

            data, errors = validate_product_payload(row)

            if errors:
                row_errors.append({
                    "row": row_number,
                    "errors": errors,
                })
            else:
                validated_rows.append(data)

        if not validated_rows and not row_errors:
            return jsonify({
                "error": "empty_csv",
                "message": "El CSV no contiene productos.",
            }), 400

        if row_errors:
            return jsonify({
                "error": "validation_error",
                "message": "No se importó ningún producto.",
                "row_errors": row_errors,
            }), 400

    except csv.Error:
        return jsonify({
            "error": "invalid_csv",
            "message": "No se pudo interpretar el archivo CSV.",
        }), 400

    try:
        service = DiscoveryService(db.session)

        created = []
        duplicates = []

        for data in validated_rows:
            result = service.discover_product(**data)

            if result.created:
                created.append(serialize_product(result.product))
            else:
                duplicates.append({
                    "product": serialize_product(result.product),
                    "reason": result.duplicate_reason,
                })

        db.session.commit()

        return jsonify({
            "total_rows": len(validated_rows),
            "created_count": len(created),
            "duplicate_count": len(duplicates),
            "created": created,
            "duplicates": duplicates,
        }), 201 if created else 200

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "error": "integrity_error",
            "message": "Conflicto de SKU o URL. No se importó ningún producto.",
        }), 409

    except Exception:
        db.session.rollback()
        raise