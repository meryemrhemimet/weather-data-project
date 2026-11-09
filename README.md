# 🌦️ Automated Weather Data Pipeline

An end-to-end Data Engineering project that collects hourly weather forecast data for Rabat, Morocco, stores it in PostgreSQL, transforms it using dbt, orchestrates the workflow with Apache Airflow, and visualizes the results using Apache Superset.

## 📌 Project Overview

This project demonstrates how to build an automated data pipeline using modern Data Engineering tools.

The pipeline retrieves weather forecast information from the **Open-Meteo API**, processes the response using Python, and stores the records in a PostgreSQL database.

The transformation process is managed by **dbt**, while **Apache Airflow** orchestrates and monitors the pipeline execution. Finally, **Apache Superset** provides a way to explore the data through charts and dashboards.

The project runs locally using **Docker Compose** and **WSL Ubuntu on Windows 11**.

## 🎯 Project Objectives

- Retrieve hourly weather forecast data for Rabat, Morocco.
- Extract temperature, weather conditions, and wind speed.
- Store weather records in a PostgreSQL database.
- Prevent duplicate records through database constraints and upsert operations.
- Transform and organize data using dbt and SQL.
- Automate and orchestrate pipeline tasks using Apache Airflow.
- Visualize weather information using Apache Superset.
- Run the services in isolated Docker containers.

## 🏗️ Architecture

```text
                  Open-Meteo API
                        |
                        v
                  Python Scripts
                (Extract and Load)
                        |
                        v
                    PostgreSQL
                  (Raw Weather Data)
                        |
                        v
                       dbt
                (SQL Transformations)
                        |
                        v
                    PostgreSQL
                 (Transformed Data)
                        |
                        v
                  Apache Superset
                 (Charts & Dashboards)


              Apache Airflow
           (Workflow Orchestration)

              Docker Compose
          (Container Management)
```

### Pipeline Workflow

1. **Data Extraction:** Python sends an HTTP request to Open-Meteo to retrieve hourly weather forecast information for Rabat.
2. **Data Processing:** The API response is parsed, weather codes are converted into readable descriptions, and records are prepared for insertion.
3. **Data Loading:** Python connects to PostgreSQL and stores the records in the raw weather table.
4. **Data Transformation:** dbt executes SQL models to create or update transformed data in PostgreSQL.
5. **Orchestration:** Airflow schedules the workflow, manages task dependencies, and monitors execution.
6. **Visualization:** Superset connects to PostgreSQL to explore the available data and create dashboards.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | API extraction and data ingestion |
| Open-Meteo API | Weather forecast data source |
| PostgreSQL | Relational database and data storage |
| psycopg2 | Python connection to PostgreSQL |
| Apache Airflow | Workflow orchestration and scheduling |
| dbt | SQL-based data transformation |
| Apache Superset | Data visualization and dashboards |
| Docker | Application containerization |
| Docker Compose | Multi-container management |
| WSL Ubuntu | Linux development environment on Windows |

## 🌍 Data Source

This project uses the free [Open-Meteo API](https://open-meteo.com/) to retrieve weather forecast data.

**Location:** Rabat, Morocco

| Parameter | Value |
|---|---|
| Latitude | 34.025 |
| Longitude | -6.836 |
| Timezone | Africa/Casablanca |
| Forecast horizon | 24 hours |
| Data frequency | Hourly |

### Weather Variables

| Variable | Description |
|---|---|
| `temperature_2m` | Air temperature at 2 metres |
| `weather_code` | Numerical weather condition code |
| `wind_speed_10m` | Wind speed at 10 metres |
| `time` | Forecast timestamp |

The API returns the information in JSON format.

**Note:** The pipeline retrieves forecast data, not historical observed weather measurements. Repeated executions may update existing city/time records as new forecast values become available.

## 📂 Project Structure

```text
weather-data-project/
│
├── api-request/
│   ├── api_request.py
│   ├── insert_records.py
│   └── requirements.txt
│
├── dags/
│   ├── orchestrator.py
│   └── dbt_orchestrator.py
│
├── dbt/
│   ├── my_project/
│   │   ├── models/
│   │   │   ├── sources.yml
│   │   │   └── ...
│   │   └── dbt_project.yml
│   │
│   └── profiles.yml.example
│
├── screenshots/
│
├── .env.example
├── .gitignore
├── docker-compose.yaml
├── README.md
└── LICENSE
```

*The structure above is a guide. Update it to match the actual files and directories in your repository.*

### Main Components

**`api_request.py`**

- Sends requests to the Open-Meteo API.
- Retrieves hourly forecast data.
- Handles HTTP errors and temporary connection failures using retry logic.
- Returns the API response as Python data.

**`insert_records.py`**

- Connects Python to PostgreSQL using psycopg2.
- Creates the raw weather table if it does not exist.
- Converts weather codes into readable descriptions.
- Inserts or updates hourly weather records.
- Uses database transactions to manage successful and failed insertions.

**`orchestrator.py`**

Defines the Airflow workflow responsible for executing the weather extraction and loading process.

**`dbt_orchestrator.py`**

Defines the Airflow task that launches a Docker container to execute dbt transformations.

**`sources.yml`**

Declares the raw PostgreSQL table as a dbt source.

**`dbt_project.yml`**

Contains the dbt project configuration.

**`profiles.yml.example`**

Provides an example of the dbt database connection configuration without exposing real credentials.

## 🔄 Data Storage

The raw weather records are stored in PostgreSQL.

**Database:** `db`

**Schema:** `dev`

**Table:** `raw_weather_data`

### Main Table Columns

| Column | Description |
|---|---|
| `id` | Unique record identifier |
| `city` | City name |
| `country` | Country name |
| `temperature` | Temperature value |
| `weather_description` | Readable weather condition |
| `wind_speed` | Wind speed |
| `time` | Forecast timestamp |
| `inserted_at` | Record insertion or update timestamp |
| `utc_offset` | UTC offset information |

A unique constraint/index on `(city, time)` prevents duplicate records for the same city and timestamp.

The ingestion process uses PostgreSQL's `ON CONFLICT` functionality to update existing records instead of inserting duplicates.

## ⚙️ Workflow Orchestration with Airflow

Apache Airflow coordinates the pipeline execution through Directed Acyclic Graphs (DAGs).

The workflow is organized around two main operations:

- **Weather ingestion task:** Executes the Python process to retrieve and load weather data.
- **Data transformation task:** Executes dbt models inside a Docker container.

Task dependencies ensure that data ingestion completes successfully before the transformation task starts.

Airflow also provides execution history, task statuses, scheduling and logs for troubleshooting.

## 🧹 Data Transformation with dbt

dbt is used to manage SQL transformations inside PostgreSQL.

The project declares `raw_weather_data` as a source and references it in SQL models using dbt's `source()` function.

Example:

```sql
SELECT *
FROM {{ source('dev', 'raw_weather_data') }}
```

dbt compiles and executes the SQL models against PostgreSQL.

The current model provides a starting point for the transformation layer. Additional models can be developed for analytical calculations, aggregations and reporting.

## 📊 Data Visualization with Superset

Apache Superset connects to the PostgreSQL project database and allows users to explore the weather data.

Possible dashboard visualizations include:

- Temperature changes over time.
- Wind speed by hour.
- Weather condition distribution.
- Hourly weather summaries.

Superset is used as the visualization layer; it reads the data stored in PostgreSQL rather than collecting weather information directly from the API.

## 🚀 Getting Started

### 1. Prerequisites

Before running the project, install:

- Windows 11
- WSL 2
- Ubuntu
- Docker Desktop
- Docker Compose
- Visual Studio Code (recommended)

Make sure Docker Desktop is configured to work with WSL 2.

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/weather-data-project.git

cd weather-data-project
```

Replace `YOUR-USERNAME` with your GitHub username.

### 3. Configure Environment Variables

Create your local environment file using the provided example:

```bash
cp .env.example .env
```

Update the environment variables with your local configuration.

Never commit your real `.env` file or database passwords.

### 4. Configure dbt

Copy the example dbt profile:

```bash
cp dbt/profiles.yml.example ~/.dbt/profiles.yml
```

Update the connection details according to your Docker Compose PostgreSQL configuration.

Make sure the database host, database name, username, password, schema and port match your environment.

### 5. Start Docker Services

From the project root:

```bash
docker-compose up -d
```

Check the running containers:

```bash
docker-compose ps
```

If you prefer to start only selected services, use the service names defined in your Compose file.

### 6. Run the Weather Ingestion Process

The ingestion script retrieves weather data from Open-Meteo and inserts it into PostgreSQL.

If the Airflow container has the project API folder mounted at `/opt/airflow/api-requests`, you can execute:

```bash
docker-compose exec af python -c 'import sys; sys.path.insert(0, "/opt/airflow/api-requests"); from insert_records import main; main()'
```

Adjust the container path if your Compose configuration mounts the folder somewhere else.

### 7. Verify the Data in PostgreSQL

Connect to PostgreSQL:

```bash
docker-compose exec db psql -U db_user -d db
```

Query the raw weather table:

```sql
SELECT *
FROM dev.raw_weather_data
ORDER BY time;
```

### 8. Execute dbt Transformations

Run:

```bash
docker-compose run --rm dbt dbt debug
```

Then execute the models:

```bash
docker-compose run --rm dbt dbt run
```

To execute configured data tests:

```bash
docker-compose run --rm dbt dbt test
```

### 9. Access Airflow

Open:

```text
http://localhost:8080
```

Use the credentials configured in your Docker Compose environment.

From the Airflow interface, you can:

- View available DAGs.
- Trigger a DAG manually.
- Monitor task execution.
- Inspect task logs.
- Check workflow execution history.

### 10. Access Superset

Open:

```text
http://localhost:8088
```

Use the credentials configured during Superset initialization.

Add a database connection to the project PostgreSQL database, select the available tables or datasets, and create visualizations.

**Important:** Superset must be configured to connect to the project database (`db`), not just its own metadata database (`superset`).

## 🔐 Security and Configuration

For safe repository sharing:

- Store passwords and sensitive configuration in environment variables.
- Keep `.env` and real credential files out of Git.
- Include only sanitized example configuration files.
- Do not commit PostgreSQL data directories or Docker volumes.
- Review files before pushing them to GitHub.


## 💡 Key Concepts Demonstrated

Through this project, I practiced and explored:

- Data ingestion from external REST APIs.
- JSON data processing with Python.
- Relational database management with PostgreSQL.
- SQL queries and database transactions.
- ELT (Extract, Load, Transform) architecture.
- SQL transformations with dbt.
- Workflow orchestration with Apache Airflow.
- Docker containerization and service networking.
- Data visualization and dashboard creation with Superset.
- Error handling and retry mechanisms.
- Avoiding duplicate records using database constraints and upserts.

## 🔮 Future Improvements

Potential improvements include:

- Add more cities and weather variables.
- Implement historical weather data collection.
- Develop staging, intermediate and analytical dbt models.
- Add dbt tests for data quality and uniqueness.
- Implement more robust logging and Airflow failure notifications.
- Add data freshness checks.
- Improve dashboard metrics and filtering.
- Deploy the pipeline to a cloud platform.
- Introduce CI/CD for automated testing and deployment.

## 📚 References

- [Open-Meteo API Documentation](https://open-meteo.com/en/docs)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [dbt Documentation](https://docs.getdbt.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Apache Superset Documentation](https://superset.apache.org/docs/)

## 👩‍💻 Author

**Meryem Rhemimet**

GitHub: @meryemrhemimet

---

*This project is a practical learning project focused on building an end-to-end data engineering pipeline using open weather forecast data.*
