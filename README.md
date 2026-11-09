# Weather Data Pipeline

This project fetches hourly weather observations from Open-Meteo, stores them in
PostgreSQL, orchestrates ingestion and dbt transformations with Airflow, and
provides a Superset service for exploring the data.

## Requirements

- Docker Engine and Docker Compose v2
- An absolute local path for this checkout, used by Airflow's Docker operator

## Start the local stack

1. Copy the example configuration files:

   ```sh
   cp .env.example .env
   cp dbt/profiles/profiles.example.yml dbt/profiles/profiles.yml
   ```

2. Set `WEATHER_PROJECT_ROOT` in `.env` to the absolute path of this directory.
3. Replace the placeholder PostgreSQL password, Superset secret key, and
   Superset admin password. These settings are for local development only.
4. Start the services from this directory:

   ```sh
   docker compose up -d --build
   ```

Airflow is available at <http://localhost:8000>, Superset at
<http://localhost:8088>, and PostgreSQL on port `5000`. The Airflow database
and Superset metadata users in `postgres/*_init.sql` use local demo
credentials; keep this stack local and change the matching initialization and
environment settings together before using it outside development.

The dbt staging model at
`dbt/my_project/models/staging/stg_weather_data.sql` deduplicates observations
by timestamp and derives local insertion time.

## GitHub copy contents

This copy contains the application source, dbt models, Docker configuration,
and database initialization scripts. It deliberately excludes virtual
environments, generated dbt output, local PostgreSQL data, and real `.env` /
dbt profile files. `.env.example` and `profiles.example.yml` are safe templates;
do not commit their local replacements.

## Push to GitHub

Create an empty repository on GitHub, then run these commands from this
directory, replacing the remote URL with your repository's URL:

```sh
git init -b main
git add .
git commit -m "Initial weather data pipeline"
git remote add origin https://github.com/<your-account>/<your-repository>.git
git push -u origin main
```
