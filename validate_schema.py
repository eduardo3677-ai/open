import json
import urllib.request
import jsonschema

with open('opencode.json', 'r') as f:
    config = json.load(f)

schema_url = 'https://opencode.ai/config.json'
with urllib.request.urlopen(schema_url) as response:
    schema = json.loads(response.read())

validator = jsonschema.Draft202012Validator(schema)
errors = list(validator.iter_errors(config))

if errors:
    print("Validation errors found:")
    for error in errors:
        print(f"  - {error.message} at {list(error.path)}")
else:
    print("JSON is valid according to the schema!")
