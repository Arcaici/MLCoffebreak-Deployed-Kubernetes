# Cassandra Table Initialization

This script (`cassandra_table_init.py`) is used to initialize the required tables in Cassandra for the CoffeBreak application. It creates a keyspace and a column family with the necessary columns.

## Prerequisites

Make sure you have the following dependencies installed:

- Python 3.x
- pandas

## Usage

1. Place the script (`cassandra_table_init.py`) in the desired directory.

2. Run the script using the following command:

   ```bash
   python cassandra_table_init.py
   ```
3. The script will create two CQL files (1_init_keyspace.cql and 2_init_columnfamily.cql) in the same directory.
4. Open a CQL shell to your Cassandra instance and execute the following commands to create the keyspace and column family:
  ```bash
  SOURCE '1_init_keyspace.cql';
  SOURCE '2_init_columnfamily.cql';
  ```
5. The keyspace caffeine and the column family new_caffeine will be created with the required columns.

## Customization

- The script expects a file named tfidf_feature_list.csv to exist in the same directory. This file should contain the list of words/features to be used as columns in the new_caffeine column family. Modify the CSV file as per your requirements.
- If you want to change the replication factor or the keyspace name, you can modify the script accordingly.
