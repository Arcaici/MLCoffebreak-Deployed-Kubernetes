FROM bitnami/cassandra
#cassandra db schema files
COPY /init_cassandra.sh ./init-scripts/init_cassandra.sh
COPY /init-scripts/1_init_keyspace.cql ./init-scripts/1_init_keyspace.cql
COPY /init-scripts/2_init_columnfamily.cql ./init-scripts/2_init_columnfamily.cql