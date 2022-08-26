# Python version of 02_do_load

import json
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer


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

i2a_schema = avro.loads(i2a_schema_str)
cd_schema = avro.loads(cd_schema_str)
key_schema = avro.loads('{"type":"string"}')


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
        if queued % 5000 == 0:
            i2aProducer.flush()
            queued = 0
i2aProducer.flush()
i2a_vals = []  # clear this because it may be a very large list

# Send callsign to destination mappings
with open("callsign-details.json") as f:
    for cd_val_str in f.readlines():
        cd_val = json.loads(cd_val_str)
        cdProducer.produce(topic='callsign-details', value=cd_val,)
cdProducer.flush()
