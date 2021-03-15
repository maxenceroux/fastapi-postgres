# FastAPI Postgres
REST operations using FastAPI Framework and PostgreSQL as database

# Add to airflow network
```sh
docker network connect airflow_default fastapi-postgres_web_1
```

# Connect to PG
```sh
docker-compose exec db sh
psql postgres -U postgres
```
