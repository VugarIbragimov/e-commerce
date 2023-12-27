# Eccomerce на faspai

my_ecommerce_app/
|-- app/
|   |-- init.py
|   |-- main.py
|   |-- auth/
|   |   |-- init.py
|   |   |-- endpoints.py
|   |   |-- models.py
|   |   |-- security.py
|   |-- products/
|   |   |-- init.py
|   |   |-- endpoints.py
|   |   |-- models.py
|   |-- reviews/
|   |   |-- init.py
|   |   |-- endpoints.py
|   |   |-- models.py
|   |-- orders/
|   |   |-- init.py
|   |   |-- endpoints.py
|   |   |-- models.py
|   |-- payments/
|   |   |-- init.py
|   |   |-- endpoints.py
|   |   |-- models.py
|-- scripts/
|   |-- consumer.py
|-- alembic/
|   |-- versions/
|-- docker/
|   |-- Dockerfile
|-- tests/
|-- config.py
|-- alembic.ini
|-- requirements.txt
|-- main.py
|-- celery_worker.py
|-- celery_config.py

what we need improve:
- add handlers for user model and set jwt-check for him
- deploy project on vps(dockerfile, compose, makefile, CI/CD)
- add sentry, grafana, promet

after all this work:

- edit file readme
- start work with other models(products, category)