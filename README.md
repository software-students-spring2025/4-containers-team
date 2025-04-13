![Lint Status](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
[![Python CI](https://github.com/software-students-spring2025/4-containers-team/actions/workflows/python-ci.yml/badge.svg)](https://github.com/software-students-spring2025/4-containers-team/actions/workflows/python-ci.yml)

# Smart Dog Feeder Dashboard

This project is a containerized full-stack application built as part of the NYU Software Engineering course. It uses image recognition to detect the presence of a person in front of a webcam. If a person is detected, the system simulates triggering a smart dog feeder to dispense food. If no person is detected, the feeder remains inactive. All detection results are stored in a MongoDB database and displayed via a web dashboard.

The system is composed of three subsystems, each running in a separate Docker container:

- A **machine learning client** that performs image recognition/classification
- A **Flask-based web application** that takes a photo and displays results 
- A **MongoDB database** that stores detection data

---

## Contributors

- [Edwin Chen](https://github.com/Eracks1012)
- [Maya Felix](https://github.com/mxf4596)
- [Andrew](https://github.com/Toudles)
- [John](https://github.com/j4ma)


## How to Set Up and Run the Project

### Prerequisites

- Docker and Docker Compose installed on your machine

### Instructions

1. **Clone the repository**

```bash
git clone https://github.com/software-students-spring2025/4-containers-team.git
cd 4-containers-team
```

2. **Build and run the containers**

```bash
docker-compose build 
docker-compose up
```

3. **Access the web application**

Open your browser and go to:

```
http://localhost:5005
```

This will display the camera and results


## Database

The MongoDB database is configured and run via Docker Compose using the official MongoDB container. It stores metadata for each detection event, including:

- Image path
- Timestamp
- Classification result (person/dog)
- Confidence score
- Whether a dog was detected (`is_dog` flag)

No starter data is required. The database is populated dynamically by the machine learning client.

## Machine Learning Client

- Implemented in Python
- Uses OpenCV and PyTorch for image capture and classification
- Classifies webcam images into either "person" or "dog"
- Automatically sends results to the MongoDB database

### Testing and CI

- Unit tests written using `pytest`
- Code formatted with `black` and linted with `pylint`
- GitHub Actions pipeline validates code on pull requests

## Web App

- Built with the Flask framework
- Connects to the MongoDB instance
- Displays detection history in a clean web dashboard

### Testing and CI

- Uses `pytest` and `pytest-flask` for unit testing
- Formatting and linting handled through GitHub Actions

