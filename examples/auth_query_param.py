from ontoportal_client import ClientConfig, OntoPortalClient

# Demonstrate query-parameter API key authentication
config = ClientConfig.from_env()
config = ClientConfig(
    base_url=config.base_url,
    api_key=config.api_key,
    auth_mode="query",
)
client = OntoPortalClient(config)

ontologies = client.list_ontologies()
print("Ontologies payload type:", type(ontologies))
