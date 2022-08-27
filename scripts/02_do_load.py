# Python version of 02_do_load

import json
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from confluent_kafka.schema_registry import SchemaRegistryClient, Schema


i2a_schema_str = """
{
    "type":"record",
    "name":"i2a",
    "fields":[
        {"name":"icao","type":"string"},
        {"name":"manufacturer","type":"string"},
        {"name":"aircraft","type":"string"},
        {"name":"type","type":"string"},
        {"name":"registration","type":"string"}
    ]
}
"""

cd_schema_str = """
{
    "type":"record",
    "name":"cd",
    "fields":[
        {"name":"callsign","type":"string"},
        {"name":"operatorname","type":"string"},
        {"name":"fromairport","type":"string"},
        {"name":"toairport","type":"string"}
    ]
}
"""

location_schema_str = """
{
    "type":"record",
    "name":"location",
    "fields":[
        {"name":"ico", "type":"string"},
        {"name":"height", "type":"string"},
        {"name":"location", "type":"string"}
    ]
}
"""

identity_schema_str = """
{
    "type":"record",
    "name":"ident",
    "fields":[
        {"name":"ico", "type":"string"},
        {"name":"identification", "type":"string"}
    ]
}
"""

i2a_schema = avro.loads(i2a_schema_str)
cd_schema = avro.loads(cd_schema_str)
key_schema = avro.loads('{"type":"string"}')
location_schema = Schema(location_schema_str, "AVRO")
identity_schema = Schema(identity_schema_str, "AVRO")


# Initialize schemas for identity, location so later table creation doesn't fail
sr_client = SchemaRegistryClient({"url": "http://localhost:8081",})
sr_client.register_schema("location-topic-value", location_schema)
sr_client.register_schema("ident-topic-value", identity_schema)


# Send ICAO/Flight number DB entries to kafka
def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


i2aProducer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'on_delivery': delivery_report,
    'schema.registry.url': 'http://localhost:8081'},
    default_key_schema=key_schema, default_value_schema=i2a_schema)

cdProducer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'on_delivery': delivery_report,
    'schema.registry.url': 'http://localhost:8081'},
    default_key_schema=key_schema, default_value_schema=cd_schema)

# Send icao to aircraft mappings
with open("icao-to-aircraft.json") as f:
    queued = 0
    for i2a_val_str in f.readlines():
        queued += 1
        i2a_val = json.loads(i2a_val_str)
        i2aProducer.produce(topic='icao-to-aircraft', value=i2a_val,)
        if queued % 10000 == 0:
            i2aProducer.flush()
            queued = 0
i2aProducer.flush()
i2a_vals = []  # clear this because it may be a very large list

# Send flight number to destination mappings
with open("callsign-details.json") as f:
    for cd_val_str in f.readlines():
        cd_val = json.loads(cd_val_str)
        cdProducer.produce(topic='callsign-details', value=cd_val,)
cdProducer.flush()
