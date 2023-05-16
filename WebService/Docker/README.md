# Caffeine Project

This repository contains the necessary configuration files to set up the Caffeine project, including a Docker Compose file and related Docker images for the application and the Cassandra database.

## Docker Compose

The Docker Compose file (`docker-compose.yml`) orchestrates the deployment of the Caffeine project using multiple services. Below are the details of the services defined in the Compose file:

### App Service

The App Service is responsible for running the Caffeine web service. It is configured as follows:

- **Image**: webservice-app:latest
- **Container Name**: caffeineapp
- **Restart Policy**: always
- **Dependencies**: cassandra
- **Environment Variables**:
  - CASSANDRA_SEEDS: cassandra
  - CASSANDRA_PASSWORD: cassandra
- **Ports**:
  - Host Port: 8000
  - Container Port: 5000
- **Command**: python main.py
- **Network**: caffeine_network

### Cassandra Service

The Cassandra Service provides the underlying database for the Caffeine project. It is configured as follows:

- **Image**: cassandra_caffeine:latest
- **Container Name**: cassandra
- **Restart Policy**: always
- **Ports**:
  - Host Port: 9042
  - Container Port: 9042
- **Volumes**:
  - Volume Name: newdata
- **Network**: caffeine_network

### Cassandra Init Service

The Cassandra Init Service runs initialization scripts for the Cassandra database. It is configured as follows:

- **Image**: cassandra_init
- **Command**: bash ./init-scripts/init_cassandra.sh
- **Dependencies**: cassandra
- **Network**: caffeine_network

## Docker Images

The Caffeine project uses several Docker images for different components. Below are the details of the Docker images used:

### webservice-app

The `webservice-app` Docker image contains the main application code and dependencies for the Caffeine web service. It is based on Python 3.9 and exposes port 5000.

### cassandra_caffeine

The `cassandra_caffeine` Docker image provides the Cassandra database for the Caffeine project. It is based on the `bitnami/cassandra` image and exposes port 9042.

### cassandra_init

The `cassandra_init` Docker image runs initialization scripts for the Cassandra database. It is also based on the `bitnami/cassandra` image.

## Initialization Scripts

The `cassandra_init` service uses the following initialization scripts for setting up the Cassandra database:

### init-scripts/init_cassandra.sh

This script initializes the Cassandra database by executing the necessary CQL statements.

### init-scripts/1_init_keyspace.cql

This CQL script creates the `caffeinedata` keyspace if it does not already exist.

### init-scripts/2_init_columnfamily.cql

This CQL script creates the `new_caffeine` column family within the `caffeinedata` keyspace.

## Volumes

The Docker Compose file defines a volume named `newdata` for persisting data related to the Cassandra database.

## Networks

The Docker Compose file defines a network named `caffeine_network` to connect the services together.

Please refer to the individual files in this repository for the complete configuration details of each component.

