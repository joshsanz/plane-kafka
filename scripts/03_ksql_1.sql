-- 3. setup stream location_stream
-- drop stream location_stream;
create stream location_stream WITH (PARTITIONS=1, kafka_topic='location-topic', value_format='AVRO');

-- 4. setup stream ident_stream
-- drop stream ident_stream;
create stream ident_stream WITH (PARTITIONS=1, kafka_topic='ident-topic', value_format='AVRO');

-- 5. combined result, location_stream join icao_to_aircraft
-- drop stream location_and_details_stream;
create stream location_and_details_stream as select l.ico, AS_VALUE(l.ico) as icao, l.height, l.location, t.aircraft, t.registration, t.manufacturer from location_stream l left join icao_to_aircraft t on l.ico = t.k_icao;

-- drop table locationtable;
-- 10s windowed reports, for deduplication?
CREATE table locationtable WITH (PARTITIONS=1, value_format='JSON', key_format='JSON') AS select ico, height, location, aircraft, registration, manufacturer, count(*) as events from location_and_details_stream WINDOW TUMBLING (size 10 second) group by ico, height, location, aircraft, registration, manufacturer;

-- 6. combined result, ident_stream join callsign
-- drop stream ident_callsign_stream;
create stream ident_callsign_stream as select i.ICO, c.operatorname, c.k_callsign, c.fromairport, c.toairport from ident_stream i left join callsign_details c on i.IDENTIFICATION = c.k_callsign;

-- drop table callsigntable;
CREATE table callsigntable WITH (PARTITIONS=1, value_format='JSON', key_format='JSON') AS select ICO, k_callsign, operatorname, fromairport, toairport, count(*) as events from ident_callsign_stream WINDOW TUMBLING (size 10 second) group by ICO, k_callsign, operatorname, fromairport, toairport;
