#!/bin/bash
echo "########################Starting to execute SH script...########################"
cd
USER_NAME='cassandra'
PASSWORD='cassandra'

cqlsh cassandra -u "${USER_NAME}" -p "${PASSWORD}" -e 'use caffeine' ;

while ! cqlsh cassandra -u "${USER_NAME}" -p "${PASSWORD}" -e 'describe cluster' ; do
     echo "########################Waiting for main instance to be ready...########################"
     sleep 1
done

for cql_file in ./init-scripts/*.cql;
do
  cqlsh cassandra -u "${USER_NAME}" -p "${PASSWORD}" -f "${cql_file}" ;
  echo "########################Script ""${cql_file}"" executed!!!########################"
done
echo "########################Execution of SH script is finished!########################"
echo "########################Stopping temporary instance!########################"