
from datetime import datetime, timezone

from app.db import db


class FinancialAnalysis(db.Model):
    __tablename__ = "financial_analyses"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    scenario = db.Column(
        db.String(30),
        nullable=False,
        index=True
    )

    currency = db.Column(
        db.String(3),
        nullable=False,
        default="USD"
    )

    landed_cost = db.Column(db.Numeric(12, 2))
    operating_cost = db.Column(db.Numeric(12, 2))
    selling_price = db.Column(db.Numeric(12, 2))

    net_profit = db.Column(db.Numeric(12, 2))
    net_margin = db.Column(db.Numeric(7, 2))
    max_cpa = db.Column(db.Numeric(12, 2))

    assumptions = db.Column(db.JSON)

    calculated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    product = db.relationship(
        "Product",
        back_populates="financial_analyses"
    )
