from app.models import Product, Evidence, Evaluation
from app.repositories import (
    ProductRepository,
    EvidenceRepository,
    EvaluationRepository,
)


def create_product(repository):
    return repository.create(
        name="Botella térmica",
        normalized_name="botella termica",
        category="Hogar",
    )


def test_product_crud_and_filtering(session):
    repo = ProductRepository(session)

    product = create_product(repo)

    assert repo.get_by_id(product.id).name == "Botella térmica"
    assert repo.get_by_normalized_name("botella termica") is not None

    updated = repo.update(product.id, status="approved")
    assert updated.status == "approved"

    assert len(repo.list(status="approved")) == 1
    assert len(repo.list(category="Electrónica")) == 0

    assert repo.delete(product.id) is True
    assert repo.get_by_id(product.id) is None


def test_evidence_crud_and_filtering(session):
    product = create_product(ProductRepository(session))
    repo = EvidenceRepository(session)

    evidence = repo.create(
        product_id=product.id,
        evidence_type="competitor",
        source="Google",
        content="Competidor con producto similar",
    )

    assert repo.get_by_id(evidence.id) is not None

    updated = repo.update(
        evidence.id,
        collection_status="failed",
        error_message="Timeout",
    )
    assert updated.collection_status == "failed"

    results = repo.list(
        product_id=product.id,
        evidence_type="competitor",
        collection_status="failed",
    )
    assert len(results) == 1

    assert repo.delete(evidence.id) is True
    assert repo.get_by_id(evidence.id) is None


def test_evaluation_crud_and_filtering(session):
    product = create_product(ProductRepository(session))
    repo = EvaluationRepository(session)

    evaluation = repo.create(
        product_id=product.id,
        ruleset_version="1.0",
        status="approved",
        hard_filters_passed=True,
        score=85,
        criteria_results={"demand": 9, "competition": 7},
        rejection_reasons=[],
    )

    assert repo.get_by_id(evaluation.id) is not None

    updated = repo.update(evaluation.id, score=90)
    assert float(updated.score) == 90.0

    results = repo.list(
        product_id=product.id,
        status="approved",
        ruleset_version="1.0",
    )
    assert len(results) == 1

    assert repo.delete(evaluation.id) is True
    assert repo.get_by_id(evaluation.id) is None