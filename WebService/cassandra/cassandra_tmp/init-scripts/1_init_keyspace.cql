CREATE KEYSPACE IF NOT EXISTS caffeinedata
  WITH REPLICATION = {
   'class' : 'SimpleStrategy',
   'replication_factor' : 1
};