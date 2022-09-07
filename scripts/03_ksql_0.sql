-- Re-process streams from the beginning to capture uploaded icao-to-aircraft mappings
SET 'auto.offset.reset' = 'earliest';

-- deprecated: see WITH for CREATE STREAM/TABLE [AS SELECT]
-- set 'ksql.sink.partitions' = '1';

-- 1. setup table icao_to_aircraft
-- drop stream icao_to_aircraft_stream;
CREATE STREAM icao_to_aircraft_stream WITH (PARTITIONS=1, KAFKA_TOPIC='icao-to-aircraft', VALUE_FORMAT='AVRO');

-- drop stream icao_to_aircraft_rekey;
CREATE STREAM icao_to_aircraft_rekey AS SELECT * FROM icao_to_aircraft_stream PARTITION BY icao;

-- DROP TABLE icao_to_aircraft;
CREATE TABLE icao_to_aircraft (K_ICAO varchar primary key) WITH (PARTITIONS=1, KAFKA_TOPIC='ICAO_TO_AIRCRAFT_REKEY', VALUE_FORMAT='AVRO');

-- 2. setup table callsign_details
-- drop stream callsign_details_stream;
CREATE STREAM callsign_details_stream WITH (PARTITIONS=1, KAFKA_TOPIC='callsign-details', VALUE_FORMAT='AVRO');

-- drop stream callsign_details_rekey;
CREATE STREAM callsign_details_rekey AS SELECT * FROM callsign_details_stream PARTITION BY callsign;

-- DROP TABLE callsign_details;
CREATE TABLE callsign_details (K_CALLSIGN varchar primary key) WITH (PARTITIONS=1, KAFKA_TOPIC='CALLSIGN_DETAILS_REKEY', VALUE_FORMAT='AVRO');