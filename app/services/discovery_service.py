from dataclasses import dataclass
from difflib import SequenceMatcher

from app.models import Product
from app.repositories import ProductRepository

from app.utils.text_cleaner import (
    normalize_product_name,
    normalize_category,
    normalize_sku,
    normalize_url,
)


@dataclass
class DiscoveryResult:
    product: Product
    created: bool
    duplicate_reason: str | None = None
    similarity: float | None = None


class DiscoveryService:
    def __init__(self, session, similarity_threshold=0.94):
        self.repository = ProductRepository(session)
        self.similarity_threshold = similarity_threshold

    @staticmethod
    def _has_conflicting_identifiers(existing, sku, url):
        if sku and existing.sku and sku != existing.sku:
            return True

        if url and existing.canonical_url and url != existing.canonical_url:
            return True

        return False

    @staticmethod
    def _has_conflicting_numbers(name_a, name_b):
        numbers_a = set(
            __import__("re").findall(r"\d+", name_a)
        )
        numbers_b = set(
            __import__("re").findall(r"\d+", name_b)
        )

        return bool(numbers_a and numbers_b and numbers_a != numbers_b)

    def find_duplicate(self, name, category=None, sku=None, url=None):
        normalized_name = normalize_product_name(name)
        normalized_category = normalize_category(category)
        normalized_sku = normalize_sku(sku)
        normalized_url = normalize_url(url)

        # 1. SKU exacto
        if normalized_sku:
            products = self.repository.list(limit=10000)

            for product in products:
                if product.sku == normalized_sku:
                    return product, "sku", 1.0

        # 2. URL exacta
        if normalized_url:
            products = self.repository.list(limit=10000)

            for product in products:
                if product.canonical_url == normalized_url:
                    return product, "url", 1.0

        # 3. Nombre normalizado exacto
        existing = self.repository.get_by_normalized_name(
            normalized_name
        )

        if existing:
            if not self._has_conflicting_identifiers(
                existing, normalized_sku, normalized_url
            ):
                return existing, "exact_name", 1.0

        # 4. Similitud textual
        candidates = self.repository.list(
            category=normalized_category,
            limit=10000,
        )

        best_match = None
        best_score = 0.0

        for product in candidates:
            if self._has_conflicting_identifiers(
                product, normalized_sku, normalized_url
            ):
                continue

            if self._has_conflicting_numbers(
                normalized_name,
                product.normalized_name,
            ):
                continue

            score = SequenceMatcher(
                None,
                normalized_name,
                product.normalized_name,
            ).ratio()

            if score >= self.similarity_threshold and score > best_score:
                best_match = product
                best_score = score

        if best_match:
            return best_match, "similarity", best_score

        return None, None, None

    def discover_product(
        self,
        *,
        name,
        category=None,
        description=None,
        sku=None,
        url=None,
    ):
        normalized_name = normalize_product_name(name)

        if not normalized_name:
            raise ValueError("El nombre del producto es obligatorio")

        normalized_category = normalize_category(category)

        normalized_sku = normalize_sku(sku)
        normalized_url = normalize_url(url)

        duplicate, reason, score = self.find_duplicate(
            name,
            category,
            sku,
            url,
        )

        if duplicate:
            return DiscoveryResult(
                product=duplicate,
                created=False,
                duplicate_reason=reason,
                similarity=score,
            )

        product = self.repository.create(
            name=name.strip(),
            normalized_name=normalized_name,
            category=normalized_category,
            description=description,
            sku=normalized_sku,
            canonical_url=normalized_url,
        )

        return DiscoveryResult(
            product=product,
            created=True,
        )