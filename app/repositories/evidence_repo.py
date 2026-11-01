from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Evidence


class EvidenceRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, **data) -> Evidence:
        evidence = Evidence(**data)
        self.session.add(evidence)
        self.session.flush()
        return evidence

    def get_by_id(self, evidence_id: int) -> Evidence | None:
        return self.session.get(Evidence, evidence_id)

    def list(
        self,
        *,
        product_id: int | None = None,
        evidence_type: str | None = None,
        collection_status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Evidence]:
        if limit < 1 or offset < 0:
            raise ValueError("limit debe ser positivo y offset no negativo")

        statement = select(Evidence)

        if product_id is not None:
            statement = statement.where(Evidence.product_id == product_id)

        if evidence_type is not None:
            statement = statement.where(
                Evidence.evidence_type == evidence_type
            )

        if collection_status is not None:
            statement = statement.where(
                Evidence.collection_status == collection_status
            )

        statement = (
            statement
            .order_by(Evidence.captured_at.desc())
            .limit(limit)
            .offset(offset)
        )

        return list(self.session.scalars(statement).all())

    def update(self, evidence_id: int, **changes) -> Evidence | None:
        evidence = self.get_by_id(evidence_id)

        if evidence is None:
            return None

        allowed_fields = {
            "evidence_type", "source", "source_url", "content",
            "extracted_data", "collection_status", "error_message"
        }

        invalid_fields = set(changes) - allowed_fields
        if invalid_fields:
            raise ValueError(f"Campos no actualizables: {invalid_fields}")

        for field, value in changes.items():
            setattr(evidence, field, value)

        self.session.flush()
        return evidence

    def delete(self, evidence_id: int) -> bool:
        evidence = self.get_by_id(evidence_id)

        if evidence is None:
            return False

        self.session.delete(evidence)
        self.session.flush()
        return True