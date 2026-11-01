
from datetime import datetime, timezone

from app.db import db


class Evaluation(db.Model):
    __tablename__ = "evaluations"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    ruleset_version = db.Column(db.String(50), nullable=False)

    status = db.Column(
        db.String(30),
        nullable=False,
        index=True
    )

    hard_filters_passed = db.Column(db.Boolean, nullable=True)

    score = db.Column(db.Numeric(7, 2))

    criteria_results = db.Column(db.JSON, nullable=False)
    rejection_reasons = db.Column(db.JSON, nullable=False)

    evaluated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    product = db.relationship(
        "Product",
        back_populates="evaluations"
    )
