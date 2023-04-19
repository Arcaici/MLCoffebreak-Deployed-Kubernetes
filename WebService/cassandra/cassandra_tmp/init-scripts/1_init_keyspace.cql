CREATE KEYSPACE IF NOT EXISTS caffeine
  WITH REPLICATION = {
   'class' : 'SimpleStrategy',
   'replication_factor' : 2
};