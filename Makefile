.PHONY: openapi-json

openapi-json:
	python -c 'import json, sys, yaml; y=yaml.safe_load(sys.stdin.read()); json.dump(y, sys.stdout, indent=2, ensure_ascii=False)' < openapi/ontoportal.yaml > openapi/ontoportal.json
