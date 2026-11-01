
from datetime import datetime, timezone

from app.db import db


class MarketExperiment(db.Model):
    __tablename__ = "market_experiments"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    name = db.Column(db.String(150), nullable=False)
    channel = db.Column(db.String(50), nullable=False)

    campaign_id = db.Column(db.String(150))
    creative_id = db.Column(db.String(150))

    impressions = db.Column(db.Integer, nullable=False, default=0)
    clicks = db.Column(db.Integer, nullable=False, default=0)
    conversions = db.Column(db.Integer, nullable=False, default=0)

    spend = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)

    currency = db.Column(db.String(3), nullable=False, default="USD")

    status = db.Column(
        db.String(30),
        nullable=False,
        default="planned"
    )

    started_at = db.Column(db.DateTime(timezone=True))
    ended_at = db.Column(db.DateTime(timezone=True))

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    notes = db.Column(db.Text)

    product = db.relationship(
        "Product",
        back_populates="experiments"
    )
