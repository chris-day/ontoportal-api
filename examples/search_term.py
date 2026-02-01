import logging

from ontoportal_client import ClientConfig, OntoPortalClient

logging.basicConfig(level=logging.INFO)

config = ClientConfig.from_env()
client = OntoPortalClient(config)

response = client.search(
    "melanoma",
    include=["prefLabel", "synonym", "definition"],
    page=1,
    pagesize=5,
)

results = response.get("collection") or response.get("results") or []
for item in results:
    print(item.get("prefLabel"), item.get("@id") or item.get("id"))
