# Python version of 01_setup_topics

from confluent_kafka.admin import AdminClient, NewTopic


a = AdminClient({'bootstrap.servers': 'localhost:9092'})

topics = ["ident-topic", "location-topic", "icao-to-aircraft", "callsign-details"]
new_topics = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in topics]
# Note: In a multi-cluster production scenario, it is more typical to use a replication_factor of 3 for durability.


# Call create_topics to asynchronously create topics. A dict
# of <topic,future> is returned.
fs = a.create_topics(new_topics)

# Wait for each operation to finish.
for topic, f in fs.items():
    try:
        f.result()  # The result itself is None
        print("Topic {} created".format(topic))
    except Exception as e:
        print("Failed to create topic {}: {}".format(topic, e))
