import requests as rq
import json
import os
import sys


def check_status(r):
    if r.status_code != 200:
        print(r.status_code, r.text)
        sys.exit(1)


schema_host = os.environ.get("SCHEMA_HOST", "http://localhost:8081")
print("Schema Host:", schema_host)

# Get list of kafka topics with schemas
r = rq.get(schema_host + "/subjects")
check_status(r)
topics = r.json()
print("Topics:", topics)

# For each topic, get schema
schemas = {}
for t in topics:
    r = rq.get('/'.join([schema_host, "subjects", t, "versions/latest"]))
    check_status(r)
    scma_meta = r.json()
    scma = json.loads(scma_meta["schema"].replace('\\"', '"'))
    schemas[t] = scma

# Print results
for t in schemas:
    print("Topic:", t)
    print(json.dumps(schemas[t], indent=2))
    print()

