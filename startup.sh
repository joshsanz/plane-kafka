#!/bin/bash

echo "####################"
echo "Bring up Docker compose project"
docker compose up -d
echo

echo "####################"
echo "Switch to script dir"
cd scripts
echo "sleeping..."
sleep 120
echo

echo "####################"
echo "Create base topics"
python 01_setup_topics.py
sleep 1
echo

echo "####################"
echo "Load ICAO database"
python 02_do_load.py
sleep 1
echo

echo "####################"
echo "Setup KSQL queries"
./03_setup_sql.sh
echo

echo "####################"
echo "Setup ElasticSearch data mappings"
./04_elastic_dynamic_template
echo

echo "####################"
echo "Setup confluent-elasticsearch connector"
./05_set_connect
echo

echo "####################"
echo "Run plane-kafka long enough to push data through pipeline"
sleep 0.5
echo

echo "####################"
echo "To finish, create indices in Kibana and make dashboard"
echo "[Hamburger Menu]->[Management]->Stack Management->[Kibana]->Index Patterns->Create index pattern"
echo "For name use location_and_details_stream, with EVENT_TS as timestamps"
sleep 0.5
echo
echo "[Hamburger Menu]->[Analytics]->Dashboard->Create new dashboard"
sleep 0.5

