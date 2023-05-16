# MLCoffebreak-Deployed-Kubernetes
CoffeBreak is a Flask-based web application that predicts the type of caffeine drink based on user input. It uses a trained machine learning model to make predictions and stores the input data in a Cassandra database.

## Prerequisites

Make sure you have the following dependencies installed:

- Python 3.x
- Flask
- NumPy
- Pandas
- scikit-learn
- Casssandra driver for Python

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/your_username/your_repository.git
```
2. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```
## Usage

1. Run the Flask application:

```bash
python main.py
```

2. Open your web browser and go to http://localhost:5000 to access the application.
3. Enter the details of your caffeine drink (name, volume, calories, and caffeine) and click "Find drink type".
4.The predicted drink type will be displayed on the page along with a description.

## Docker

A DockerCompose file of the CoffeBreak application is available on this repository. You can run the application inside Docker containers using the following command:
```bash
dockercompose up ./path/to/dockercompose.yaml
```
Remember to build docker images from docker files with command:
```bash
docker build -t image_name ./path/to/Dockerfile
```

## Kubernetes
A Kubernetes deployment and service configuration file is available in the repository (coffe_break.yaml). You can use this file to deploy the CoffeBreak application on a Kubernetes cluster using the following command:

```bash
kubectl apply -f coffee_break.yaml
```

The application will be deployed as a service that can be accesible using:

```bash
kubectl port-forward -n caffeine deployment/caffeine-ws 8080:5000
```

Then open your browser and go to "http://localhost:8080"

## Further Documentation
Here are the links to the Docker and Kubernetes versions and model:

- [Docker version](https://github.com/Arcaici/MLCoffebreak-Deployed-Kubernetes/tree/main/WebService)
- [Kubernetes version](https://github.com/Arcaici/MLCoffebreak-Deployed-Kubernetes/tree/main/WebService/Docker)
- [Model](https://github.com/Arcaici/MLCoffebreak-Deployed-Kubernetes/tree/main/model)
