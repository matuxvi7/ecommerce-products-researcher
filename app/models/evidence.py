
from datetime import datetime, timezone

from app.db import db


class Evidence(db.Model):
    __tablename__ = "evidences"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    evidence_type = db.Column(db.String(50), nullable=False, index=True)
    source = db.Column(db.String(150), nullable=False)
    source_url = db.Column(db.Text)

    content = db.Column(db.Text)
    extracted_data = db.Column(db.JSON)

    captured_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    collection_status = db.Column(
        db.String(30),
        nullable=False,
        default="success"
    )

    error_message = db.Column(db.Text)

    product = db.relationship(
        "Product",
        back_populates="evidences"
    )
