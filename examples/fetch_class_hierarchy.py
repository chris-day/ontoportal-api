import logging

from ontoportal_client import ClientConfig, OntoPortalClient, encode_class_iri

logging.basicConfig(level=logging.INFO)

config = ClientConfig.from_env()
client = OntoPortalClient(config)

acronym = "SNOMEDCT"
class_iri = "http://snomed.info/id/24700007"

cls = client.get_class(acronym, class_iri)
print("Class:", cls.get("prefLabel"), cls.get("@id") or cls.get("id"))

children = client.follow_link(cls, "children") or {}
child_items = children.get("collection") or children.get("results") or []
print("Children count:", len(child_items))

parents = client.follow_link(cls, "parents") or {}
parent_items = parents.get("collection") or parents.get("results") or []
print("Parents count:", len(parent_items))

# Demonstrate manual link traversal if a link is a raw URL
links = cls.get("_links") or cls.get("links") or {}
children_link = links.get("children")
if isinstance(children_link, dict) and "href" in children_link:
    print("Children link URL:", children_link["href"])

# Demonstrate explicit class IRI encoding
print("Encoded IRI:", encode_class_iri(class_iri))
