
from datetime import datetime, timezone

from app.db import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)
    normalized_name = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    category = db.Column(db.String(100), index=True)
    description = db.Column(db.Text)

    status = db.Column(
        db.String(30),
        nullable=False,
        default="candidate",
        index=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    evidences = db.relationship(
        "Evidence",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    evaluations = db.relationship(
        "Evaluation",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    financial_analyses = db.relationship(
        "FinancialAnalysis",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    experiments = db.relationship(
        "MarketExperiment",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    sku = db.Column(
        db.String(100),
        unique=True,
        index=True,
        nullable=True,
    )

    canonical_url = db.Column(
        db.String(2048),
        unique=True,
        index=True,
        nullable=True,
    )

    def __repr__(self):
        return f"<Product {self.id}: {self.name}>"