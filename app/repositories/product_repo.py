from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Product


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, **data) -> Product:
        product = Product(**data)
        self.session.add(product)
        self.session.flush()
        return product

    def get_by_id(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)

    def get_by_normalized_name(self, normalized_name: str) -> Product | None:
        statement = select(Product).where(
            Product.normalized_name == normalized_name
        )
        return self.session.scalar(statement)

    def list(
        self,
        *,
        category: str | None = None,
        status: str | None = None,
        search: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Product]:
        if limit < 1 or offset < 0:
            raise ValueError("limit debe ser positivo y offset no negativo")

        statement = select(Product)

        if category is not None:
            statement = statement.where(Product.category == category)

        if status is not None:
            statement = statement.where(Product.status == status)

        if search:
            statement = statement.where(Product.name.ilike(f"%{search}%"))

        statement = (
            statement
            .order_by(Product.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        return list(self.session.scalars(statement).all())

    def update(self, product_id: int, **changes) -> Product | None:
        product = self.get_by_id(product_id)

        if product is None:
            return None

        allowed_fields = {
            "name", "normalized_name", "category",
            "description", "status"
        }

        invalid_fields = set(changes) - allowed_fields
        if invalid_fields:
            raise ValueError(f"Campos no actualizables: {invalid_fields}")

        for field, value in changes.items():
            setattr(product, field, value)

        self.session.flush()
        return product

    def delete(self, product_id: int) -> bool:
        product = self.get_by_id(product_id)

        if product is None:
            return False

        self.session.delete(product)
        self.session.flush()
        return True