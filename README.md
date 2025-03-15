# Flask - creating API part 8

## About

This repository is my eighth homework assignment from the Python Pro course. 

My task was to implement Docker into the project. 
Docker is a platform for developing, shipping, and running applications in containers. 
Containers package software and its dependencies, ensuring consistent environments across different system

 - Added dockerfile
 - Added docker-compose.yml

## How to Run

1. Clone the repository:  
   ```bash
   git clone https://github.com/OleksiiUzu/flask-api-homework-8-docker.git
   cd flask-api-homework-8-docker
   
2.(Optional) Create and activate a virtual environment:
  python -m venv venv
  source venv/bin/activate
  
3.Build the Docker image: 
 docker build -t flask-app .

4.Run the container: 
 docker run -p 5000:5000 flask-app
