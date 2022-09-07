FROM confluentinc/cp-server-connect:7.2.1
# FROM cnfldemos/cp-server-connect-datagen:0.5.3-7.1.0

RUN confluent-hub install --no-prompt confluentinc/kafka-connect-elasticsearch:14.0.0
RUN confluent-hub install --no-prompt confluentinc/connect-transforms:latest
