from unittest.mock import Mock

from ontoportal_client.client import OntoPortalClient
from ontoportal_client.config import ClientConfig
from ontoportal_client.http import HttpClient


def test_paginate_with_links_next_page():
    config = ClientConfig(api_key="abc")
    http = HttpClient(config)

    first = {
        "collection": [1, 2],
        "_links": {"nextPage": {"href": "https://data.bioontology.org/ontologies?page=2"}},
    }
    second = {"collection": [3]}

    http.request = Mock(side_effect=[first, second])

    client = OntoPortalClient(config=config, http=http)
    items = list(client.paginate("/ontologies"))

    assert items == [1, 2, 3]


def test_paginate_with_page_count():
    config = ClientConfig(api_key="abc")
    http = HttpClient(config)

    page1 = {"page": 1, "pageCount": 2, "collection": ["a"]}
    page2 = {"page": 2, "pageCount": 2, "collection": ["b"]}

    http.request = Mock(side_effect=[page1, page2])

    client = OntoPortalClient(config=config, http=http)
    items = list(client.paginate("/search", params={"q": "x"}))

    assert items == ["a", "b"]
