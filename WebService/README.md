# Caffeine Project

This repository contains the necessary configuration files to set up the Caffeine project, which includes a StatefulSet for Cassandra, a Deployment for a web service, a Pod for NGINX, and related Services. These components are deployed within the "caffeine" namespace.

## Cassandra StatefulSet

The Cassandra StatefulSet is responsible for managing a single replica of the Cassandra database. The StatefulSet ensures the availability and durability of the data. Below are the details of the Cassandra StatefulSet configuration:

- **Name**: caffeine-cassandra
- **Namespace**: caffeine
- **Labels**: app: caffeine-db
- **Replicas**: 1
- **Selector**:
  - Match Labels: app: caffeine-db
- **Containers**:
  - **Name**: cassandra-caffeine
  - **Image**: cassandra_caffeine
  - **Image Pull Policy**: Never
  - **Environment Variables**:
    - CASSANDRA_SEEDS: caffeine-cassandra-0
  - **Ports**:
    - Container Port: 9042
  - **Volume Mounts**:
    - Name: caffeine-pvc
      - Mount Path: /var/cassandra/data

## Cassandra Service

The Cassandra Service allows external access to the Cassandra database. It is configured as follows:

- **Name**: caffeine-service-db
- **Namespace**: caffeine
- **Selector**: app: caffeine-db
- **Cluster IP**: None
- **Ports**:
  - Protocol: TCP
  - Port: 9042
  - Target Port: 9042

## Persistent Volume Claim

The Persistent Volume Claim (PVC) ensures persistent storage for the Cassandra database. The PVC is configured as follows:

- **Name**: caffeine-pvc
- **Namespace**: caffeine
- **Access Modes**:
  - ReadWriteOnce
- **Resources**:
  - Requests:
    - Storage: 100Mi

## Web Service Deployment

The Web Service Deployment manages two replicas of the Caffeine web service. The Deployment configuration is as follows:

- **Name**: caffeine-ws
- **Namespace**: caffeine
- **Labels**: app: caffeine-app
- **Replicas**: 2
- **Selector**:
  - Match Labels: app: caffeine-app
- **Containers**:
  - **Name**: web-service
  - **Image**: webservice-app
  - **Image Pull Policy**: Never
  - **Ports**:
    - Container Port: 5000

## Web Service Service

The Web Service Service enables external access to the Caffeine web service. It is configured as follows:

- **Name**: caffeine-service-ws
- **Namespace**: caffeine
- **Selector**: app: caffeine-app
- **Type**: LoadBalancer
- **Ports**:
  - Protocol: TCP
  - Port: 5000
  - Target Port: 5000
  - Node Port: 30100

## NGINX Pod

The NGINX Pod hosts a single instance of the NGINX server. The Pod configuration is as follows:

- **Name**: nginx-pod
- **Namespace**: caffeine
- **Containers**:
  - **Name**: nginx-container
  - **Image**: nginx
  - **Ports**:
    - Container Port: 80

## Test Service

The Test Service allows external access to the Caffeine application for testing purposes. It is configured as follows:

- **Name**: test
- **Namespace**: caffeine
- **Selector**: app: caffeine-db
- **Cluster IP**: None
- **Ports**:
    - Protocol: TCP
    - Port: 80
    - Target Port: 80

