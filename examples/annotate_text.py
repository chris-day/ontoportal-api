import logging

from ontoportal_client import ClientConfig, OntoPortalClient

logging.basicConfig(level=logging.INFO)

config = ClientConfig.from_env()
client = OntoPortalClient(config)

text = "Patient has melanoma and underwent excision."

response = client.annotator(
    text,
    ontologies=["SNOMEDCT"],
)

print("Annotations:", len(response))
for ann in response[:3]:
    matched = ann.get("annotatedClass", {}).get("prefLabel")
    print("Match:", matched)
