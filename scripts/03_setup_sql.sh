#!/bin/bash

cd ../test
docker compose exec ksqldb-cli bash -c "ksql --file /scripts/03_ksql_0.sql -- http://ksqldb-server:8088"
echo "sleeping..."
sleep 3
docker compose exec ksqldb-cli bash -c "ksql --file /scripts/03_ksql_1.sql -- http://ksqldb-server:8088"

