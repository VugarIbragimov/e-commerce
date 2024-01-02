# E-commerce 

E-commerce project. An application framework that can be adapted for a future real project.

### **Technology stack**
![python version](https://img.shields.io/badge/Python-3.9.6-red)
![fastapi version](https://img.shields.io/badge/aiogram-0.88.0-green)
![uvicorn version](https://img.shields.io/badge/uvicorn-0.20.0-purple)
![SQLAlchemy version](https://img.shields.io/badge/SQLAlchemy==-1.4.45-black)
![alembic version](https://img.shields.io/badge/alembic==-1.9.0-green)
![pydantic version](https://img.shields.io/badge/pydantic==-2.5.3-pink)
![PostgreSQL version](https://img.shields.io/badge/PostgreSQL-14.1-blue)
![docker version](https://img.shields.io/badge/Docker-20.10.7-blue)
![Sentry version](https://img.shields.io/badge/Sentry-23.7.1-orange)
![Prometheus version](https://img.shields.io/badge/Prometheus-2.43.0-orange)
![Grafana version](https://img.shields.io/badge/Grafana-8.5.22-orange)

### Installation
Clone the repository and go to it on the command line:
```
git clone git@github.com:VugarIbragimov/e-commerce.git
```
Launch a project via Docker
```
docker-compose -f docker-compose-local.yaml up
```
Run migrations to the database(before these, you should create an alembic.ini file)
```
docker-compose -f docker-compose-local.yaml exec fast_app alembic upgrade heads
```
### API
Here you can view the endpoints API documentation
### link to the API: http://89.104.70.208:8080/docs#/

### Monitoring with Prometheus and Grafan
Login and password for enter to the grafana (admin:admin)
### link to the Prometheus http://89.104.70.208:9090/
### link to the Grafana http://89.104.70.208:3000/

# !!!
The project will evolve gradually and change over time. if you have comments and suggestions, I will be glad to listen to you!
### https://telegram.me/iamlilze
