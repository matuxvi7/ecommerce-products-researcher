from app.models import Product
from app.services.discovery_service import DiscoveryService
from app.utils.text_cleaner import (
    normalize_product_name,
    normalize_category,
    normalize_url,
)


def test_normalize_product_name():
    assert normalize_product_name(
        "  BOTELLA Térmica  "
    ) == "botella termica"


def test_normalize_category():
    aliases = {
        "tecnologia": "Electrónica",
        "electronica": "Electrónica",
    }

    assert normalize_category(
        "Tecnología",
        aliases,
    ) == "Electrónica"


def test_normalize_url():
    assert normalize_url(
        "https://www.tienda.com/producto?utm_source=ads"
    ) == "https://tienda.com/producto"


def test_exact_duplicate_is_not_created(session):
    service = DiscoveryService(session)

    first = service.discover_product(
        name="Botella Térmica",
        category="Hogar",
    )

    second = service.discover_product(
        name=" BOTELLA TERMICA ",
        category="Hogar",
    )

    assert first.created is True
    assert second.created is False
    assert first.product.id == second.product.id

    assert session.query(Product).count() == 1


def test_sku_duplicate_is_detected(session):
    service = DiscoveryService(session)

    service.discover_product(
        name="Botella Térmica",
        sku="BT-001",
    )

    result = service.discover_product(
        name="Botella de acero inoxidable",
        sku="bt-001",
    )

    assert result.created is False
    assert result.duplicate_reason == "sku"


def test_url_duplicate_is_detected(session):
    service = DiscoveryService(session)

    service.discover_product(
        name="Botella Térmica",
        url="https://www.tienda.com/producto?utm_source=ads",
    )

    result = service.discover_product(
        name="Botella de acero",
        url="https://tienda.com/producto",
    )

    assert result.created is False
    assert result.duplicate_reason == "url"


def test_similar_product_is_detected(session):
    service = DiscoveryService(session)

    service.discover_product(
        name="Botella termica de acero inoxidable",
        category="Hogar",
    )

    result = service.discover_product(
        name="Botella termica acero inoxidable",
        category="Hogar",
    )

    assert result.created is False
    assert result.duplicate_reason == "similarity"


def test_different_variants_are_not_merged(session):
    service = DiscoveryService(session)

    service.discover_product(
        name="Botella térmica 500 ml",
        category="Hogar",
    )

    result = service.discover_product(
        name="Botella térmica 1000 ml",
        category="Hogar",
    )

    assert result.created is True
    assert session.query(Product).count() == 2

def test_same_name_with_different_skus_is_allowed(session):
    service = DiscoveryService(session)

    first = service.discover_product(
        name="Botella térmica",
        sku="BT-500",
    )

    second = service.discover_product(
        name="Botella térmica",
        sku="BT-1000",
    )

    assert first.created is True
    assert second.created is True
    assert first.product.id != second.product.id
    assert session.query(Product).count() == 2