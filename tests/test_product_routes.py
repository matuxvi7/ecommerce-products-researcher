import io

from app.models import Product


def test_create_product(client):
    response = client.post(
        "/api/products",
        json={
            "name": "Botella térmica",
            "category": "Hogar",
            "sku": "BT-001",
        },
    )

    assert response.status_code == 201
    assert response.json["created"] is True
    assert response.json["product"]["name"] == "Botella térmica"


def test_create_duplicate_product(client):
    payload = {
        "name": "Botella térmica",
        "sku": "BT-001",
    }

    first = client.post("/api/products", json=payload)
    second = client.post("/api/products", json=payload)

    assert first.status_code == 201
    assert second.status_code == 200
    assert second.json["created"] is False


def test_create_product_without_name(client):
    response = client.post(
        "/api/products",
        json={"category": "Hogar"},
    )

    assert response.status_code == 400
    assert response.json["error"] == "validation_error"


def test_import_csv(client, session):
    csv_content = (
        "name,category,sku\n"
        "Botella térmica,Hogar,BT-001\n"
        "Auriculares,Electrónica,AU-001\n"
    )

    response = client.post(
        "/api/products/import-csv",
        data={
            "file": (
                io.BytesIO(csv_content.encode("utf-8")),
                "products.csv",
            )
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 201
    assert response.json["created_count"] == 2
    assert session.query(Product).count() == 2


def test_import_csv_is_atomic(client, session):
    csv_content = (
        "name,category\n"
        "Botella térmica,Hogar\n"
        ",Electrónica\n"
    )

    response = client.post(
        "/api/products/import-csv",
        data={
            "file": (
                io.BytesIO(csv_content.encode("utf-8")),
                "invalid.csv",
            )
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.json["error"] == "validation_error"
    assert session.query(Product).count() == 0


def test_import_csv_detects_duplicates(client):
    csv_content = (
        "name,category,sku\n"
        "Botella térmica,Hogar,BT-001\n"
        "Botella térmica,Hogar,BT-001\n"
    )

    response = client.post(
        "/api/products/import-csv",
        data={
            "file": (
                io.BytesIO(csv_content.encode("utf-8")),
                "duplicates.csv",
            )
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 201
    assert response.json["created_count"] == 1
    assert response.json["duplicate_count"] == 1