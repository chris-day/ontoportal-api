import os
import pytest

from ontoportal_client import ClientConfig, OntoPortalClient


BIOPORTAL_API_KEY = os.getenv("BIOPORTAL_API_KEY")

pytestmark = pytest.mark.skipif(
    not BIOPORTAL_API_KEY, reason="BIOPORTAL_API_KEY not set; skipping live API tests"
)


def _client():
    config = ClientConfig.from_env()
    return OntoPortalClient(config)


def test_live_list_ontologies():
    client = _client()
    data = client.list_ontologies(params={"page": 1, "pagesize": 1})
    assert isinstance(data, (dict, list))
    if isinstance(data, dict):
        assert "collection" in data or "results" in data
    else:
        assert len(data) > 0


def test_live_search():
    client = _client()
    data = client.search("melanoma", pagesize=1)
    assert isinstance(data, dict)
    assert "collection" in data or "results" in data


def test_live_class_fetch():
    client = _client()
    data = client.search("melanoma", pagesize=5)
    results = data.get("collection") or data.get("results") or []
    if not results:
        pytest.skip("No search results returned; skipping class fetch")

    # Try to follow annotatedClass link when available (most robust across portals)
    annotated = results[0].get("annotatedClass") if isinstance(results[0], dict) else None
    if annotated and isinstance(annotated, dict):
        cls = client.follow_link(annotated, "self")
        if cls:
            assert isinstance(cls, dict)
            assert cls.get("prefLabel") or cls.get("@id") or cls.get("id")
            return

    pytest.skip("No annotatedClass link available for class fetch")
