from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Evaluation


class EvaluationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, **data) -> Evaluation:
        evaluation = Evaluation(**data)
        self.session.add(evaluation)
        self.session.flush()
        return evaluation

    def get_by_id(self, evaluation_id: int) -> Evaluation | None:
        return self.session.get(Evaluation, evaluation_id)

    def list(
        self,
        *,
        product_id: int | None = None,
        status: str | None = None,
        ruleset_version: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Evaluation]:
        if limit < 1 or offset < 0:
            raise ValueError("limit debe ser positivo y offset no negativo")

        statement = select(Evaluation)

        if product_id is not None:
            statement = statement.where(
                Evaluation.product_id == product_id
            )

        if status is not None:
            statement = statement.where(Evaluation.status == status)

        if ruleset_version is not None:
            statement = statement.where(
                Evaluation.ruleset_version == ruleset_version
            )

        statement = (
            statement
            .order_by(Evaluation.evaluated_at.desc())
            .limit(limit)
            .offset(offset)
        )

        return list(self.session.scalars(statement).all())

    def update(self, evaluation_id: int, **changes) -> Evaluation | None:
        evaluation = self.get_by_id(evaluation_id)

        if evaluation is None:
            return None

        allowed_fields = {
            "ruleset_version", "status", "hard_filters_passed",
            "score", "criteria_results", "rejection_reasons"
        }

        invalid_fields = set(changes) - allowed_fields
        if invalid_fields:
            raise ValueError(f"Campos no actualizables: {invalid_fields}")

        for field, value in changes.items():
            setattr(evaluation, field, value)

        self.session.flush()
        return evaluation

    def delete(self, evaluation_id: int) -> bool:
        evaluation = self.get_by_id(evaluation_id)

        if evaluation is None:
            return False

        self.session.delete(evaluation)
        self.session.flush()
        return True