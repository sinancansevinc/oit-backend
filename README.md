
# Dockerized Django, Postgres, Celery, Nginx and RabbitMQ!

This is a template project that can be used to start a new django project easily.



## Requirements
You need to have **Docker** engine and **Docker Compose** to run this project.

Check out these links for installing them:

https://docs.docker.com/engine/install/

https://docs.docker.com/compose/install/
    
## Running the project

Clone the repository

```
git clone git@github.com:DoktorTakvimi/oit-backend.git
```
Create an **.env** file similar to **env.txt** at root directory

Start using docker compose
```
cd oit-backend
docker compose up -d
```

Visit your browser for admin panel
```
http://localhost/admin
```

Visit your browser for api endpoints
```
http://localhost/api
```

## Usage/Examples
Create a super user
```
docker exec -it api python manage.py createsuperuser
```

Create a new django app
```python
docker exec -it api python manage.py startapp <your-app-name>
```
Start building your api endpoints!